import pytest
import json
from tests.resources.test_support.controls import telescope_is_in_off_state, telescope_is_in_on_state, telescope_is_in_standby_state, subarray_obs_state_is_empty, subarray_obs_state_is_idle
import tests.resources.test_support.tmc_helpers as tmc
from tests.conftest import LOGGER
from tests.resources.test_support.tmc_helpers import tear_down
from tests.resources.test_support.helpers import waiter
from tango import DeviceProxy

scan_file= "command_Scan.json"
assign_resources_file = "command_AssignResources.json"
release_resources_file  = "command_ReleaseResources.json"

@pytest.mark.SKA_mid
def test_scan_not_allowed_in_idle():
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
        assign_res_input = tmc.get_input_str(assign_resources_file)
        tmc.compose_sub(assign_res_input)

        """Verify ObsState is Idle"""
        # Given a Subarray in IDLE observation state
        assert subarray_obs_state_is_idle()
        scan_input = tmc.get_input_str(scan_file)
        subarray_node = DeviceProxy("ska_mid/tm_subarray_node/1")
        with pytest.raises(Exception) as info:
        # When SCAN command invoked
            subarray_node.Scan(scan_input)
        # Then it fails with Command not Allowed error
        assert "Scan command not permitted in observation state IDLE" in str(info.value)
        # And TMC remains in IDLE observation state
        assert subarray_obs_state_is_idle()
        """Invoke ReleaseResources() command on TMC"""
        release_input_str = tmc.get_input_str(release_resources_file)
        tmc.invoke_releaseResources(release_input_str)
        assert subarray_obs_state_is_empty()

        """Invoke TelescopeStandby() command on TMC"""
        tmc.set_to_standby()

        """Verify State transitions after TelescopeStandby"""
        assert telescope_is_in_standby_state()
    except Exception:
        release_json = tmc.get_input_str(release_resources_file)
        tear_down(release_json)
