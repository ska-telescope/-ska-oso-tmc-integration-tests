import pytest
from tests.resources.test_support.controls import telescope_is_in_off_state, telescope_is_in_on_state, telescope_is_in_standby_state, subarray_obs_state_is_empty, subarray_obs_state_is_idle
import tests.resources.test_support.tmc_helpers as tmc
from tests.conftest import LOGGER
from tests.resources.test_support.helpers import waiter
from tango import DeviceProxy

scan_file= "command_Scan.json"
assign_resources_file = "command_AssignResources.json"
release_resources_file  = "command_ReleaseResources.json"

@pytest.mark.SKA_mid
@pytest.mark.skip(reason="The test is skipped as there is no exception raised for off command when called in idle state in current implementation")
def test_off_not_allowed_in_idle():  

    # try: 
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
    assign_res_input = tmc.get_input_str(assign_resources_file)
    tmc.compose_sub(assign_res_input)

    """Verify ObsState is Idle"""
    # Given a Subarray in IDLE observation state
    assert subarray_obs_state_is_idle()
    # tmc.set_to_off()
    fixture["state"] ="AssignResources"
    subarray_node = DeviceProxy("ska_mid/tm_subarray_node/1")
    # subarray_node.Off()
    # scan_input = tmc.get_input_str(scan_file)            
    # central_node = DeviceProxy("ska_mid/tm_central/central_node")
    # central_node.TelescopeOff()
    with pytest.raises(Exception) as info:
    # # When OFF command invoked
        subarray_node.Off()
    # # Then it fails with Command not Allowed error
    assert "OFF command not permitted in observation state IDLE" in str(info.value)
    # And TMC remains in IDLE observation state
    assert subarray_obs_state_is_idle()
    """Invoke ReleaseResources() command on TMC"""
    release_input_str = tmc.get_input_str(release_resources_file)
    tmc.invoke_releaseResources(release_input_str)

    fixture["state"] = "ReleaseResources"
    assert subarray_obs_state_is_empty()

    """Invoke TelescopeOff() command on TMC"""
    tmc.set_to_off()

    """Verify State transitions after TelescopeOff"""
    assert telescope_is_in_off_state()
    fixture["state"] = "TelescopeOff"
