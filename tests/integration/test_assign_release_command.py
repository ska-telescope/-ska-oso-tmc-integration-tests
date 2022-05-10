import pytest
from tests.resources.test_support.controls import telescope_is_in_standby_state, telescope_is_in_on_state, telescope_is_in_off_state, subarray_obs_state_is_empty, subarray_obs_state_is_idle
import tests.resources.test_support.tmc_helpers as tmc, get_input_str
from tests.conftest import LOGGER

assign_resources_file = "command_AssignResources.json"
release_resources_file  = "command_ReleaseResources.json"

@pytest.mark.SKA_mid
def test_assign_release_commands():
    """AssignResources and ReleaseResources is executed."""
    try:
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
        
        """Verify ObsState is Empty"""
        assert subarray_obs_state_is_empty()

        assign_input_str = get_input_str(assign_resources_file)

        """Invoke AssignResources() Command on TMC"""
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")
        tmc.set_to_assign_resources(assign_input_str)
        LOGGER.info("AssignResources command is invoked successfully")
 
        """Verify ObsState is Idle"""
        assert subarray_obs_state_is_idle()
        fixture["state"] ="AssignResources"

        release_input_str = get_input_str(release_resources_file)
        
        """Invoke ReleaseResources() command on TMC"""
        tmc.invoke_releaseResources(release_input_str)

        fixture["state"] = "ReleaseResources"
        assert subarray_obs_state_is_empty()

        """Invoke TelescopeOff() command on TMC"""
        tmc.set_to_off()

        """Verify State transitions after TelescopeOff"""
        assert telescope_is_in_off_state()
        fixture["state"] = "TelescopeOff"

        LOGGER.info("Tests complete: tearing down...")

    except:
        LOGGER.info("Exception occurred in the test for state = {}".format(fixture["state"]))
        if fixture["state"] == "AssignResources":
            tmc.invoke_releaseResources(release_input_str)
        if fixture["state"] == "TelescopeOn":
            tmc.set_to_off()
        raise