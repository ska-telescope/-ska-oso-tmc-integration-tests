import pytest
from tango import DeviceProxy
from tests.resources.test_support.constant_low import *
from tests.resources.test_support.low.controls import (telescope_is_in_standby_state,
        telescope_is_in_on_state, telescope_is_in_off_state,
        subarray_obs_state_is_resourcing,
        subarray_obs_state_is_aborted, subarray_obs_state_is_empty,subarray_obs_state_is_idle,)
import tests.resources.test_support.low.tmc_helpers as tmc
from tests.conftest import LOGGER

@pytest.mark.SKA_low
def test_low_abort_restart_in_resourcing(json_factory):
    """Abort and Restart is executed."""
    try:
        assign_json = json_factory("command_assign_resource_low")
        release_json = json_factory("command_release_resource_low")
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

        """Verify ObsState is IDLE"""
        assert subarray_obs_state_is_idle()
        fixture["state"] ="AssignResources"
        central_node = DeviceProxy(centralnode)
        central_node.AssignResources(assign_json)

        # """Invoke Abort() command on TMC"""
        tmc.invoke_abort()

        fixture["state"] = "Abort"
        assert subarray_obs_state_is_aborted()

        """Invoke Restart() command on TMC"""
        tmc.invoke_restart()

        fixture["state"] = "Restart"
        """Verify ObsState is EMPTY"""
        assert subarray_obs_state_is_empty()

        """Invoke TelescopeOff() command on TMC"""
        tmc.set_to_off()

        """Verify State transitions after TelescopeOff"""
        assert telescope_is_in_off_state()
        fixture["state"] = "TelescopeOff"

        LOGGER.info("Tests complete.")

    except:
        if fixture["state"] == "AssignResources":
            tmc.invoke_releaseResources(release_json)
        if fixture["state"] == "TelescopeOn":
            tmc.set_to_off()
        raise
