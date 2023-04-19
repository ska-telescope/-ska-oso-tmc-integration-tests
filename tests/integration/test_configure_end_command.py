import json

import pytest
from tango import DeviceProxy

import tests.resources.test_support.tmc_helpers as tmc
from tests.conftest import LOGGER
from tests.resources.test_support.constant import (
    centralnode,
    tmc_subarraynode1,
)
from tests.resources.test_support.controls import (
    subarray_obs_state_is_empty,
    subarray_obs_state_is_idle,
    subarray_obs_state_is_ready,
    telescope_is_in_off_state,
    telescope_is_in_on_state,
    telescope_is_in_standby_state,
)
from tests.resources.test_support.helpers import resource
from tests.resources.test_support.sync_decorators import (
    sync_assign_resources,
    sync_configure,
    sync_end,
)
from tests.resources.test_support.tmc_helpers import tear_down

assign_resources_file = "command_AssignResources.json"
release_resources_file = "command_ReleaseResources.json"
configure_resources_file = "command_Configure.json"


@pytest.mark.SKA_mid
def test_configure_end():
    """Configure and End is executed."""
    try:
        """Verify Telescope is Off/Standby"""
        assert telescope_is_in_standby_state()
        LOGGER.info("Staring up the Telescope")

        """Invoke TelescopeOn() command on TMC"""
        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
        tmc.set_to_on()
        LOGGER.info("TelescopeOn command is invoked successfully")

        """Verify State transitions after TelescopeOn"""
        assert telescope_is_in_on_state()

        """Invoke AssignResources() Command on TMC"""
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")

        @sync_assign_resources()
        def compose_sub():
            resource(tmc_subarraynode1).assert_attribute("State").equals("ON")
            resource(tmc_subarraynode1).assert_attribute("obsState").equals(
                "EMPTY"
            )
            assign_res_input = tmc.get_input_str(assign_resources_file)
            central_node = DeviceProxy(centralnode)
            central_node.AssignResources(assign_res_input)
            LOGGER.info("Invoked AssignResources on CentralNode")

        compose_sub()

        """Verify ObsState is Idle"""
        assert subarray_obs_state_is_idle()
        LOGGER.info("AssignResources command is invoked successfully")

        """Invoke Configure() Command on TMC"""
        LOGGER.info("Invoking Configure command on TMC CentralNode")

        @sync_configure()
        def configure_subarray():
            resource(tmc_subarraynode1).assert_attribute("obsState").equals(
                "IDLE"
            )
            configure_input = tmc.get_input_str(configure_resources_file)
            subarray_node = DeviceProxy("ska_mid/tm_subarray_node/1")
            subarray_node.Configure(configure_input)
            LOGGER.info("Invoked Configure on SubarrayNode")

        configure_subarray()

        """Verify ObsState is READY"""
        assert subarray_obs_state_is_ready()
        LOGGER.info("Configure command is invoked successfully")

        """Invoke End() Command on TMC"""
        LOGGER.info("Invoking End command on TMC SubarrayNode")

        @sync_end()
        def end():
            resource(tmc_subarraynode1).assert_attribute("obsState").equals(
                "READY"
            )
            subarray_node = DeviceProxy(tmc_subarraynode1)
            subarray_node.End()
            LOGGER.info("Invoked End on SubarrayNode")

        end()

        """Verify ObsState is IDLE"""
        assert subarray_obs_state_is_idle()
        LOGGER.info("End command is invoked successfully")

        release_input_str = tmc.get_input_str(release_resources_file)

        """Invoke ReleaseResources() command on TMC"""
        tmc.invoke_releaseResources(release_input_str)

        assert subarray_obs_state_is_empty()

        """Invoke TelescopeStandby() command on TMC"""
        tmc.set_to_standby()

        """Verify State transitions after TelescopeStandby"""
        assert telescope_is_in_standby_state()

        LOGGER.info("Tests complete.")

    except Exception:
        release_json = tmc.get_input_str(release_resources_file)
        tear_down(release_json)
