import pytest
from tests.resources.test_support.low.controls import telescope_is_in_standby_state, telescope_is_in_on_state, telescope_is_in_off_state, subarray_obs_state_is_empty, subarray_obs_state_is_idle
import tests.resources.test_support.low.tmc_helpers as tmc
from tests.conftest import LOGGER
from tests.resources.test_support.low.sync_decorators import sync_assign_resources
from tests.resources.test_support.low.helpers import resource
from tests.resources.test_support.constant_low import tmc_subarraynode1, centralnode
from tango import DeviceProxy


@pytest.mark.xfail(reason="Validate this test case after Image of Subarray Device is released with Assign and Release resource command")
@pytest.mark.SKA_low
def test_assign_release_low(json_factory):
    """AssignResources and ReleaseResources is executed."""
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
        @sync_assign_resources()
        def compose_sub():
            resource(tmc_subarraynode1).assert_attribute("State").equals(
                "ON"
            )
            resource(tmc_subarraynode1).assert_attribute("obsState").equals(
                "EMPTY"
            )            
            central_node = DeviceProxy(centralnode)
            tmc.check_devices()
            central_node.AssignResources(assign_json)
            LOGGER.info("Invoked AssignResources on CentralNode")

        compose_sub()

        LOGGER.info("AssignResources command is invoked successfully")
 
        """Verify ObsState is Idle"""
        assert subarray_obs_state_is_idle()
        fixture["state"] ="AssignResources"
        
        """Invoke ReleaseResources() command on TMC"""
        tmc.invoke_releaseResources(release_json)

        fixture["state"] = "ReleaseResources"
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

