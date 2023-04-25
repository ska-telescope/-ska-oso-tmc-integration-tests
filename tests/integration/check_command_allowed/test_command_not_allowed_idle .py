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
    DEVICE_STATE_OFF_INFO
)
from tests.resources.test_support.mid.telescope_controls_mid import TelescopeControlMid
from tests.resources.test_support.common_utils.tmc_helpers import TmcHelper
from tests.conftest import LOGGER

configure_resources_file = "command_Configure.json"
assign_resources_file = "command_AssignResources.json"
scan_file = "command_Scan.json"

@pytest.mark.SKA_mid
@scenario("../features/check_command_not_allowed.feature",
          "Unexpected commands not allowed when TMC subarray is idle")
def test_command_not_valid_in_idle():
    """
    fucntion to check validation
    """


@given("the TMC is in ON state and the subarray is in IDLE")
def given_tmc(json_factory):
    # Verify Telescope is Off/Standby
    tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)

    """Verify Telescope is Off/Standby"""
    assert telescope_is_in_standby_state()
    LOGGER.info("Starting up the Telescope")

    # Invoke TelescopeOn() command on TMC
    LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
    tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)
    LOGGER.info("TelescopeOn command is invoked successfully")

    # Verify State transitions after TelescopeOn
    assert telescope_is_in_on_state()
    assert subarray_obs_state_is_empty()

    # Invoke AssignResources() Command on TMC

    LOGGER.info("Invoking AssignResources command on TMC CentralNode")

    # Invoke AssignResources() Command on TMC

    telescope_control = TelescopeControlMid()

    assign_json = json_factory("command_AssignResources")
    # Invoke AssignResources() Command on TMC
    LOGGER.info("Invoking AssignResources command on TMC CentralNode")
    tmc_helper.compose_sub(assign_json, **ON_OFF_DEVICE_COMMAND_DICT)
    LOGGER.info("AssignResources command is invoked successfully")

    # Verify ObsState is IDLE#
    assert telescope_control.is_in_valid_state(DEVICE_OBS_STATE_IDLE_INFO, "obsState")

    # Verify ObsState is Idle
    assert subarray_obs_state_is_idle()
    LOGGER.info("IDLE is invoked successfully")

    # Verify ObsState is Idle
    assert subarray_obs_state_is_idle()


@when(parsers.parse("the command {unexpected_command} is invoked on the/that subarray"))
def send(json_factory, unexpected_command):
    # use try expect
    tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)
    Scan_json = json_factory("command_Scan")
    try:
        if unexpected_command == 'Scan':
            LOGGER.info("Invoking Scan command on TMC SubarrayNode")
            tmc_helper.scan(Scan_json, **ON_OFF_DEVICE_COMMAND_DICT)
        elif unexpected_command == 'End':
            LOGGER.info("Invoking Scan command on TMC SubarrayNode")
            tmc_helper.end()
        else:
            LOGGER.info("Other invalid commands")
    except:
        LOGGER.info("INVALID COMMAND INVOKED")


@then(parsers.parse("the TMC should reject the {unexpected_command} with ResultCode.Rejected"))
def invalid_command_rejection():
    pass


@then("TMC subarray remains in IDLE obsState")
def tmc_status():
    telescope_control = TelescopeControlMid()
    # assert telescope_control.is_in_valid_state(DEVICE_STATE_ON_INFO, "State")
    assert telescope_control.is_in_valid_state(DEVICE_OBS_STATE_IDLE_INFO, "obsState")


@then("TMC executes the RealeaseResources command successfully")
def tmc_accepts_next_commands(json_factory):
    
    tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)
    telescope_control = TelescopeControlMid()

    # Invoke RealeaseResources() Command on TMC
    release_json = json_factory("command_ReleaseResources")
    LOGGER.info("Invoking ReleaseResources command on TMC CentralNode")
    tmc_helper.invoke_releaseResources(release_json, **ON_OFF_DEVICE_COMMAND_DICT)
    # Invoke TelescopeOff() command on TMC#
    tmc_helper.set_to_off(**ON_OFF_DEVICE_COMMAND_DICT)

    # Verify State transitions after TelescopeOff#
    assert telescope_control.is_in_valid_state(DEVICE_STATE_OFF_INFO, "State")
    assert telescope_control.is_in_valid_state(DEVICE_OBS_STATE_EMPTY_INFO, "obsState")

    """Invoke TelescopeStandby() command on TMC"""
    tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)
