import pytest

import tests.resources.test_support.tmc_helpers as tmc
from tests.conftest import LOGGER
from tests.resources.test_support.constant import tmc_subarraynode1
from tests.resources.test_support.controls import (
    check_subarray1_availability,
    subarray_obs_state_is_empty,
    subarray_obs_state_is_idle,
    subarray_obs_state_is_ready,
    telescope_is_in_on_state,
    telescope_is_in_standby_state,
)
from tests.resources.test_support.tmc_helpers import tear_down

assign_resources_file = "command_AssignResources.json"
release_resources_file = "command_ReleaseResources.json"
configure_resources_file = "command_Configure.json"
scan_file = "command_Scan.json"


@pytest.mark.skip(
    reason="Scan command is not implemented on SDP Subarray Leaf Node."
)
@pytest.mark.SKA_mid
def test_scan_endscan():
    """Scan and EndScan is executed."""
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

        # Check Subarray1 availability
        assert check_subarray1_availability(tmc_subarraynode1)

        # # Invoke AssignResources() Command on TMC
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")
        assign_res_input = tmc.get_input_str(assign_resources_file)
        tmc.compose_sub(assign_res_input)

        # # Verify ObsState is Idle
        assert subarray_obs_state_is_idle()

        # # Invoke Configure() Command on TMC
        LOGGER.info("Invoking Configure command on TMC CentralNode")
        configure_input_str = tmc.get_input_str(configure_resources_file)
        tmc.configure_subarray(configure_input_str)

        # # Verify ObsState is READY
        assert subarray_obs_state_is_ready()

        # # Invoke Scan() Command on TMC
        LOGGER.info("Invoking Scan command on TMC CentralNode")
        scan_input = tmc.get_input_str(scan_file)
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
