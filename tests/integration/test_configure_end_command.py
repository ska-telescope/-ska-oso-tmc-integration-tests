import pytest
from tests.resources.test_support.controls import telescope_is_in_standby_state, telescope_is_in_on_state, telescope_is_in_off_state, subarray_obs_state_is_empty, subarray_obs_state_is_idle, subarray_obs_state_is_ready
import tests.resources.test_support.tmc_helpers as tmc
from tests.conftest import LOGGER
from tests.resources.test_support.sync_decorators import sync_assign_resources, sync_configure, sync_end
from tests.resources.test_support.helpers import resource
from tango import DeviceProxy


assign_resources_file = "command_AssignResources.json"
release_resources_file  = "command_ReleaseResources.json"
configure_resources_file = "command_Configure.json" 

@pytest.mark.SKA_mid
def test_configure_end():
    """Configure and End is executed."""
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
    
        """Invoke AssignResources() Command on TMC"""
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")
        @sync_assign_resources()
        def compose_sub():
            resource("ska_mid/tm_subarray_node/1").assert_attribute("State").equals(
                "ON"
            )
            resource("ska_mid/tm_subarray_node/1").assert_attribute("obsState").equals(
                "EMPTY"
            )
            assign_res_input = tmc.get_input_str(assign_resources_file)            
            central_node = DeviceProxy("ska_mid/tm_central/central_node")
            central_node.AssignResources(assign_res_input)
            LOGGER.info("Invoked AssignResources on CentralNode")

        compose_sub()

        """Verify ObsState is Idle"""
        assert subarray_obs_state_is_idle()
        fixture["state"] ="AssignResources"
        LOGGER.info("AssignResources command is invoked successfully")

        """Invoke Configure() Command on TMC"""
        LOGGER.info("Invoking Configure command on TMC CentralNode")
        @sync_configure()
        def configure_subarray():
            resource("ska_mid/tm_subarray_node/1").assert_attribute("obsState").equals(
                "IDLE"
            )
            configure_input = tmc.get_input_str(configure_resources_file)            
            subarray_node = DeviceProxy("ska_mid/tm_subarray_node/1")
            subarray_node.Configure(configure_input)
            LOGGER.info("Invoked Configure on SubarrayNode")

        configure_subarray()

        """Verify ObsState is READY"""
        assert subarray_obs_state_is_ready()
        fixture["state"] ="Configure"
        LOGGER.info("Configure command is invoked successfully")

        """Invoke End() Command on TMC"""
        LOGGER.info("Invoking End command on TMC SubarrayNode")
        @sync_end()
        def end():
            resource("ska_mid/tm_subarray_node/1").assert_attribute("obsState").equals(
                "READY"
            )
            subarray_node = DeviceProxy("ska_mid/tm_subarray_node/1")
            subarray_node.End()
            LOGGER.info("Invoked End on SubarrayNode")

        end()

        """Verify ObsState is IDLE"""
        assert subarray_obs_state_is_idle()
        fixture["state"] ="End"
        LOGGER.info("End command is invoked successfully")


        release_input_str = tmc.get_input_str(release_resources_file)
        
        """Invoke ReleaseResources() command on TMC"""
        tmc.invoke_releaseResources(release_input_str)

        fixture["state"] = "ReleaseResources"
        assert subarray_obs_state_is_empty()

        """Invoke TelescopeOff() command on TMC"""
        tmc.set_to_off()

        """Verify State transitions after TelescopeOff"""
        assert telescope_is_in_off_state()
        fixture["state"] = "TelescopeOff"

        LOGGER.info("Tests complete.")

    except:
        LOGGER.info("Exception occurred in the test for state = {}".format(fixture["state"]))
        LOGGER.info("Tearing down...")
        if fixture["state"] == "AssignResources":
            tmc.invoke_releaseResources(release_input_str)
        if fixture["state"] == "TelescopeOn":
            tmc.set_to_off()
        raise