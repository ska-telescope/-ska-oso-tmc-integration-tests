"""
AssignResourcesCommand class for TMC Mid

"""
import pytest
from tests.resources.test_support.controls import (
    telescope_is_in_standby_state, 
    telescope_is_in_on_state, 
    subarray_obs_state_is_idle,
    subarray_obs_state_is_empty,
)
import tests.resources.test_support.tmc_helpers as tmc
from tests.conftest import LOGGER


@pytest.mark.SKA_mid
def test_assign_resources():
    """AssignResources is executed."""
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

        """Invoke AssignResources() Command on TMC"""
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")
        tmc.set_to_assign_resources()
        LOGGER.info("AssignResources command is invoked successfully")
 
        """Verify ObsState is Idle"""
        assert subarray_obs_state_is_idle()
        fixture["state"] ="AssignResources"
        

    except:
        LOGGER.info("Exception occurred in the test for state = {}".format(fixture["state"]))
        if fixture["state"] == "TelescopeOn":
            tmc.set_to_off()
        raise