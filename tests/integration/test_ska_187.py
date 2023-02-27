import pytest
import json
from tests.resources.test_support.controls import (telescope_is_in_standby_state,
        telescope_is_in_on_state, telescope_is_in_off_state,
        subarray_obs_state_is_idle,
        subarray_obs_state_is_aborted, subarray_obs_state_is_empty)
import tests.resources.test_support.tmc_helpers as tmc
from tests.conftest import LOGGER
from tests.resources.test_support.sync_decorators import sync_configure_abort
from tests.resources.test_support.helpers import resource
from tango import DeviceProxy

@pytest.mark.skip(reason = "This scenario is no longer valid because CDM is taking care of schema validation.")
@pytest.mark.SKA_mid
def test_skb_187_abort_restart(json_factory):
    """Unhappy scenario: Subarray stucks in Configuring with invalid json(SKB-187)
    Abort and Restart is executed to bring Subarray to initial obsState"""
    try:
        assign_json = json_factory("command_AssignResources")
        release_json = json_factory("command_ReleaseResources")
        tmc.check_devices()
        fixture = {}
        fixture["state"] = "Unknown"

        """Verify Telescope is Off/Standby"""
        assert telescope_is_in_standby_state()
        LOGGER.info("Staring up the Telescope")

        """Invoke TelescopeOn() command on TMC"""
        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
        tmc.set_to_on()
        LOGGER.info("TelescopeOn command is invoked successfully")

        """Verify State transitions after TelescopeOn"""
        assert telescope_is_in_on_state()
        fixture["state"] = "TelescopeOn"

        """Invoke AssignResources() Command on TMC"""
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")
        tmc.compose_sub(assign_json)
        LOGGER.info("AssignResources command is invoked successfully")

        """Verify ObsState is Idle"""
        assert subarray_obs_state_is_idle()
        fixture["state"] ="AssignResources"
        LOGGER.info("AssignResources command is invoked successfully")

        """Invoke Configure() Command on TMC"""
        LOGGER.info("Invoking Configure command on TMC SubarrayNode")
        @sync_configure_abort()
        def configure_subarray():
            resource("ska_mid/tm_subarray_node/1").assert_attribute("obsState").equals(
                "IDLE"
            )
            subarray_node = DeviceProxy("ska_mid/tm_subarray_node/1")
            subarray_node.Configure("{}")
            LOGGER.info("Invoked Configure on SubarrayNode")
        configure_subarray()

        # with invalid configure json, Tmc subarray stuck in Configuring
        resource("ska_mid/tm_subarray_node/1").assert_attribute("obsState").equals(
                "CONFIGURING"
            )
        fixture["state"] ="Configure"
        LOGGER.info("AssignResources command is invoked successfully")

        """Invoke Abort() Command on TMC"""
        LOGGER.info("Invoking Abort command on TMC SubarrayNode")
        tmc.invoke_abort()
        assert subarray_obs_state_is_aborted()
        fixture["state"] ="Abort"

        """Invoke Restart() Command on TMC"""
        LOGGER.info("Invoking Restart command on TMC SubarrayNode")
        tmc.invoke_restart()
        assert subarray_obs_state_is_empty()
        fixture["state"] ="Restart"

        """Invoke TelescopeOff() Command on TMC"""
        LOGGER.info("Invoking TelescopeOff command on TMC CentralNode")
        tmc.set_to_off()
        assert telescope_is_in_off_state()
        fixture["state"] ="TelescopeOff"

    except:
        LOGGER.info("Tearing down failed test, state = {}".format(fixture["state"]))
        if fixture["state"] == "AssignResources":
            tmc.invoke_releaseResources(release_json)
            raise Exception("unable to teardown subarray from being in AssignResources")
        if fixture["state"] == "Configure":
            tmc.invoke_abort()
            tmc.invoke_restart()
            tmc.set_to_off()
            raise Exception("unable to teardown subarray from being in Configure")
        if fixture["state"] == "TelescopeOn":
            tmc.set_to_off()
            raise Exception("unable to teardown subarray from being in TelescopeOn")
        pytest.fail("unable to complete test without exceptions")

