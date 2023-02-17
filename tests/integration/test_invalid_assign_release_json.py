import pytest
from tests.resources.test_support.controls import telescope_is_in_standby_state, telescope_is_in_on_state, telescope_is_in_off_state, subarray_obs_state_is_empty, subarray_obs_state_is_idle
import tests.resources.test_support.tmc_helpers as tmc
from tests.conftest import LOGGER
from tests.resources.test_support.helpers import resource, waiter
from tango import DeviceProxy

@pytest.mark.aki
@pytest.mark.SKA_mid
def test_assign_invalid_json(json_factory):
    """AssignResources and ReleaseResources is executed."""
    assign_json = json_factory("command_invalid_assign")
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
    resource("ska_mid/tm_subarray_node/1").assert_attribute("State").equals(
        "ON"
    )
    resource("ska_mid/tm_subarray_node/1").assert_attribute("obsState").equals(
        "EMPTY"
    )            
    central_node = DeviceProxy("ska_mid/tm_central/central_node")
    tmc.check_devices()
    ret_code, message = central_node.AssignResources(assign_json)

   #Assert with TaskStatus as REJECTED
    assert ret_code == 5
    LOGGER.info(message)

    """Verify ObsState is Idle"""
    assert telescope_is_in_on_state()

    # """Invoke TelescopeOff() command on TMC"""
    tmc.set_to_off()

    # """Verify State transitions after TelescopeOff"""
    assert telescope_is_in_off_state()
    fixture["state"] = "TelescopeOff"

    # LOGGER.info("Tests complete.")


def test_release_invalid_json(json_factory):
    """AssignResources and ReleaseResources is executed."""
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_invalid_release")
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

    """Invoke Releaseesources() Command on TMC"""
    LOGGER.info("Invoking ReleaseResources command on TMC CentralNode")
    resource("ska_mid/tm_subarray_node/1").assert_attribute("State").equals(
        "ON"
    )
    resource("ska_mid/tm_subarray_node/1").assert_attribute("obsState").equals(
        "RESOURCING"
    )            
    central_node = DeviceProxy("ska_mid/tm_central/central_node")
    tmc.check_devices()
    ret_code, message = central_node.ReleaseResources(release_json)

    #Assert with TaskStatus as REJECTED
    assert ret_code == 5
    LOGGER.info(message)

    """Verify ObsState is Empty"""
    assert telescope_is_in_on_state()

    # """Invoke TelescopeOff() command on TMC"""
    tmc.set_to_off()

    # """Verify State transitions after TelescopeOff"""
    assert telescope_is_in_off_state()
    fixture["state"] = "TelescopeOff"

    # LOGGER.info("Tests complete.")

