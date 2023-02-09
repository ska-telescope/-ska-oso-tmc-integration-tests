import pytest
from tests.resources.test_support.controls import telescope_is_in_standby_state, telescope_is_in_on_state, telescope_is_in_off_state, subarray_obs_state_is_empty, subarray_obs_state_is_idle
import tests.resources.test_support.tmc_helpers as tmc
from tests.conftest import LOGGER
from tests.resources.test_support.sync_decorators import sync_assign_resources
from tests.resources.test_support.helpers import resource, waiter
from tango import DeviceProxy
from ska_control_model import HealthState
@pytest.mark.SKA_mid_skip
def test_assign_release(json_factory):
    """AssignResources and ReleaseResources is executed."""
    try:
        assign_json = json_factory("command_AssignResources")
        release_json = json_factory("command_ReleaseResources")
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
            resource("ska_mid/tm_subarray_node/1").assert_attribute("State").equals(
                "ON"
            )
            resource("ska_mid/tm_subarray_node/1").assert_attribute("obsState").equals(
                "EMPTY"
            )            
            central_node = DeviceProxy("ska_mid/tm_central/central_node")
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

@pytest.mark.SKA_mid
def test_health_check():
    """Health Check of CSP and SDP devices"""

    cspsubarrayleaf_node_dev = DeviceProxy("ska_mid/tm_leaf_node/csp_subarray01")
    csp_subarray_leafnode_healthState = (
        cspsubarrayleaf_node_dev.read_attribute("healthState").value
    )
    assert csp_subarray_leafnode_healthState == HealthState.OK

    central_node = DeviceProxy("ska_mid/tm_central/central_node")
    central_node_healthState = (
        central_node.read_attribute("healthState").value
    )
    assert central_node_healthState == HealthState.OK

    csp_master_dev_name = "mid-csp/control/0"

    csp_master_dev = DeviceProxy(csp_master_dev_name)
    csp_master_dev_healthState = (
        csp_master_dev.read_attribute("healthState").value
    )
    assert csp_master_dev_healthState == HealthState.OK