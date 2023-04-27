import pytest

import tests.resources.test_support.tmc_helpers as tmc
from tests.conftest import LOGGER
from tests.resources.test_support.controls import (
    subarray_obs_state_is_empty,
    subarray_obs_state_is_idle,
    subarray_obs_state_is_ready,
    telescope_is_in_on_state,
    telescope_is_in_standby_state,
)
from tests.resources.test_support.tmc_helpers import tear_down

assign_resources_file = "command_AssignResources.json"
release_resources_file = "command_ReleaseResources.json"
configure_json = "command_Configure.json"
configure_json_2 = "command_Configure_2.json"
configure_json_3 = "command_Configure_3.json"
scan_json = "command_Scan.json"
scan_json_2 = "command_Scan_2.json"
scan_json_3 = "command_Scan_3.json"


@pytest.mark.SKA_mid
@pytest.mark.MS2
def test_successive_scan_with_different_configurations():
    """Successive Scan command with different configurations."""
    try:

        # Verify Telescope is Off/Standby
        assert telescope_is_in_standby_state()
        LOGGER.info("Staring up the Telescope")

        # # Invoke TelescopeOn() command on TMC
        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
        tmc.set_to_on()
        LOGGER.info("TelescopeOn command is invoked successfully")

        # # Verify State transitions after TelescopeOn
        assert telescope_is_in_on_state()

        # # Invoke AssignResources() Command on TMC
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")
        assign_res_input = tmc.get_input_str(assign_resources_file)
        tmc.compose_sub(assign_res_input)

        # # Verify ObsState is Idle
        assert subarray_obs_state_is_idle()

        # # Invoke Configure() Command on TMC
        LOGGER.info("Invoking Configure command on TMC CentralNode")
        configure_input_str = tmc.get_input_str(configure_json)
        tmc.configure_subarray(configure_input_str)

        # # Verify ObsState is READY
        assert subarray_obs_state_is_ready()

        # # Invoke Scan() Command on TMC
        LOGGER.info("Invoking Scan command on TMC CentralNode")
        scan_input = tmc.get_input_str(scan_json)
        tmc.scan(scan_input)

        # # Verify ObsState is READY
        assert subarray_obs_state_is_ready()

        # # Invoke End() Command on TMC
        LOGGER.info("Invoking End command on TMC SubarrayNode")
        tmc.end()

        # # Verify ObsState is IDLE
        assert subarray_obs_state_is_idle()

        # # Invoke Configure() Command on TMC
        LOGGER.info("Invoking Configure command on TMC CentralNode")
        configure_input_str = tmc.get_input_str(configure_json_2)
        tmc.configure_subarray(configure_input_str)

        # # Verify ObsState is READY
        assert subarray_obs_state_is_ready()

        # # Invoke Scan() Command on TMC
        LOGGER.info("Invoking Scan command on TMC CentralNode")
        scan_input = tmc.get_input_str(scan_json_2)
        tmc.scan(scan_input)

        # # Verify ObsState is READY
        assert subarray_obs_state_is_ready()

        # # Invoke End() Command on TMC
        LOGGER.info("Invoking End command on TMC SubarrayNode")
        tmc.end()

        # # Verify ObsState is IDLE
        assert subarray_obs_state_is_idle()

        # # Invoke Configure() Command on TMC
        LOGGER.info("Invoking Configure command on TMC CentralNode")
        configure_input_str = tmc.get_input_str(configure_json_3)
        tmc.configure_subarray(configure_input_str)

        # # Verify ObsState is READY
        assert subarray_obs_state_is_ready()

        # # Invoke Scan() Command on TMC
        LOGGER.info("Invoking Scan command on TMC CentralNode")
        scan_input = tmc.get_input_str(scan_json_3)
        tmc.scan(scan_input)

        # # Verify ObsState is READY
        assert subarray_obs_state_is_ready()

        # # Invoke End() Command on TMC
        LOGGER.info("Invoking End command on TMC SubarrayNode")
        tmc.end()

        # # Verify ObsState is IDLE
        assert subarray_obs_state_is_idle()

        # # Invoke ReleaseResources() command on TMC
        release_input_str = tmc.get_input_str(release_resources_file)
        tmc.invoke_releaseResources(release_input_str)

        assert subarray_obs_state_is_empty()

        # # Invoke TelescopeStandby() command on TMC
        tmc.set_to_standby()

        # # Verify State transitions after TelescopeStandby
        assert telescope_is_in_standby_state()

    except Exception:
        release_json = tmc.get_input_str(release_resources_file)
        tear_down(release_json)
