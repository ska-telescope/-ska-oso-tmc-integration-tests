import pytest
import tango
from pytest_bdd import given, parsers, scenario, then, when
from tests.resources.test_support.controls import telescope_is_in_standby_state, telescope_is_in_on_state, \
    telescope_is_in_off_state, subarray_obs_state_is_empty, subarray_obs_state_is_idle, subarray_obs_state_is_ready
from tests.resources.test_support.common_utils.sync_decorators import sync_assign_resources, sync_configure, sync_end
from tango import DeviceProxy
from tests.resources.test_support.constant import (
    tmc_subarraynode1,
    centralnode,
    ON_OFF_DEVICE_COMMAND_DICT,
    DEVICE_STATE_ON_INFO,
    DEVICE_OBS_STATE_EMPTY_INFO,
    DEVICE_OBS_STATE_IDLE_INFO,
    DEVICE_STATE_OFF_INFO, DEVICE_OBS_STATE_READY_INFO,
)
from tests.resources.test_support.mid.telescope_controls_mid import TelescopeControlMid
from tests.resources.test_support.common_utils.tmc_helpers import TmcHelper
from tests.conftest import LOGGER
from tests.resources.test_support.tmc_helpers import tear_down


tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)
telescope_control = TelescopeControlMid()

@pytest.mark.SKA_mid
@scenario("../features/check_command_not_allowed.feature",
          "Unexpected commands not allowed when TMC subarray is idle")
def test_command_not_valid_in_idle_obsState():
    """
    Test commands not allowed in SubarrayNode obsState.IDLE

    """


@given("the TMC is in ON state and the subarray is in IDLE")
def given_tmc(json_factory):
    # Verify Telescope is Off/Standby
    assert telescope_is_in_standby_state()
    LOGGER.info("Starting up the Telescope")

    # Invoke TelescopeOn() command on TMC
    LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
    tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)
    LOGGER.info("TelescopeOn command is invoked successfully")

    # Verify State transitions after TelescopeOn 
    assert telescope_control.is_in_valid_state(DEVICE_STATE_ON_INFO, "State")
    assert telescope_control.is_in_valid_state(DEVICE_OBS_STATE_EMPTY_INFO, "obsState")

    assign_json = json_factory("command_AssignResources")
    LOGGER.info("Invoking AssignResources command on TMC CentralNode")
    tmc_helper.compose_sub(assign_json, **ON_OFF_DEVICE_COMMAND_DICT)
    LOGGER.info("AssignResources command is invoked successfully")

    # Verify ObsState is IDLE
    assert telescope_control.is_in_valid_state(DEVICE_OBS_STATE_IDLE_INFO, "obsState")


@when(parsers.parse("the command {unexpected_command} is invoked on that subarray"))
def send(json_factory, unexpected_command):
    scan_json = json_factory("command_Scan")
    try:
        LOGGER.info("Invoking Scan command on TMC SubarrayNode")
        tmc_helper.scan(scan_json, **ON_OFF_DEVICE_COMMAND_DICT)
    except Exception as e:
        LOGGER.info(f"Exception occured: {e}")


# TODO: Current version of TMC does not support ResultCode.REJECTED, 
# once the implementation is introduced, below block will be updated.
@then(parsers.parse("the TMC should reject the {unexpected_command} with ResultCode.Rejected"))
def invalid_command_rejection(unexpected_command):
    pass


@then("TMC subarray remains in IDLE obsState")
def tmc_status():
    # Verify SubarrayNode obsState
    assert telescope_control.is_in_valid_state(DEVICE_OBS_STATE_IDLE_INFO, "obsState")


@then(parsers.parse("TMC executes the {permitted_command} command successfully"))
def tmc_accepts_next_commands(json_factory, permitted_command):
    configure_json = json_factory("command_Configure")
    release_json = json_factory("command_ReleaseResources")
    if permitted_command == "Configure":
        LOGGER.info(f"permitted command is: {permitted_command}")
        LOGGER.info("Invoking Configure command on TMC CentralNode")
        tmc_helper.configure_sub(configure_json, **ON_OFF_DEVICE_COMMAND_DICT)
        assert telescope_control.is_in_valid_state(DEVICE_OBS_STATE_READY_INFO, "obsState")
        # tear down
        tear_down(release_json)
    elif permitted_command == "ReleaseResources":
        LOGGER.info(f"permitted command is: {permitted_command}")
        LOGGER.info("Invoking ReleaseResources command on TMC CentralNode")
        tmc_helper.invoke_releaseResources(release_json, **ON_OFF_DEVICE_COMMAND_DICT)
        assert telescope_control.is_in_valid_state(DEVICE_OBS_STATE_EMPTY_INFO, "obsState")
        # tear down
        tear_down()
        # assert telescope_control.is_in_valid_state(DEVICE_STATE_OFF_INFO, "State")
    else:
        LOGGER.info(f"permitted command is: {permitted_command}")
