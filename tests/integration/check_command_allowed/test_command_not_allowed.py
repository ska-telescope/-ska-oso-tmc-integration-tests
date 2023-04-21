import pytest
from pytest_bdd import given, parsers, scenario, then, when

from tests.conftest import LOGGER
from tests.resources.test_support.common_utils.tmc_helpers import TmcHelper
from tests.resources.test_support.constant import (
    centralnode,
    tmc_subarraynode1,

    ON_OFF_DEVICE_COMMAND_DICT,
    DEVICE_STATE_ON_INFO,
    DEVICE_OBS_STATE_EMPTY_INFO,
    DEVICE_OBS_STATE_IDLE_INFO,
    DEVICE_STATE_OFF_INFO
)
from tests.resources.test_support.controls import telescope_is_in_on_state, subarray_obs_state_is_empty
from tests.resources.test_support.controls import telescope_is_in_standby_state
from tests.resources.test_support.mid.telescope_controls_mid import TelescopeControlMid

configure_resources_file = "command_Configure.json"
assign_resources_file = "command_AssignResources.json"


@pytest.mark.SKA_mid
@scenario("../features/check_command_not_allowed.feature",
          "Invalid unexpected commands not allowed in the current stable obsState")
def test_command_not_valid_in_empty():
    """
    fucntion to check validation
    """


@given(parsers.parse("the TMC device/s state=On and obsState {initial_obsstate}"))
def given_tmc():
    """Verify Telescope is Off/Standby"""
    tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)

    """Verify Telescope is Off/Standby"""
    assert telescope_is_in_standby_state()
    LOGGER.info("Starting up the Telescope")

    """Invoke TelescopeOn() command on TMC"""
    LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
    tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)
    LOGGER.info("TelescopeOn command is invoked successfully")

    """Verify State transitions after TelescopeOn"""
    assert telescope_is_in_on_state()
    assert subarray_obs_state_is_empty()


@when(
    parsers.parse("the command {unexpected_command} is invoked , throws an error"))
def send(json_factory, unexpected_command):
    # use try expect
    tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)
    Scan_json = json_factory("command_Scan")
    Configure_json = json_factory("command_Configure")
    try:
        if unexpected_command == 'Configure':
            LOGGER.info("Invoking Configure command on TMC CentralNode")
            # TmcHelper.configure_subarray(Configure_json, **ON_OFF_DEVICE_COMMAND_DICT)
            tmc_helper.configure_subarray(Configure_json, **ON_OFF_DEVICE_COMMAND_DICT)
        elif unexpected_command == 'Scan':
            LOGGER.info("Invoking Scan command on TMC CentralNode")
            # TmcHelper.scan(Scan_json, **ON_OFF_DEVICE_COMMAND_DICT)
            tmc_helper.scan(Scan_json, **ON_OFF_DEVICE_COMMAND_DICT)
        elif unexpected_command == 'End':
            LOGGER.info("Invoking Scan command on TMC CentralNode")
            tmc_helper.end()
        else:
            LOGGER.info("Other invalid commands")
    except:
        LOGGER.info('CONFIGURE COMMAND NOT VALID IN EMPTY ObsState ')


@then(parsers.parse("the TMC device remains in state=On, and obsState {initial_obsstate}"))
def tmc_status(initial_obsstate):
    telescope_control = TelescopeControlMid()
    assert telescope_control.is_in_valid_state(DEVICE_STATE_ON_INFO, "State")
    assert telescope_control.is_in_valid_state(DEVICE_OBS_STATE_EMPTY_INFO, "obsState")


@then(parsers.parse("TMC accepts correct/expected command {expected_command} and performs the operation"))
def tmc_accepts_next_commands(json_factory):
    """Invoke AssignResources() Command on TMC"""

    tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)
    telescope_control = TelescopeControlMid()

    assign_json = json_factory("command_AssignResources")
    # Invoke AssignResources() Command on TMC#
    LOGGER.info("Invoking AssignResources command on TMC CentralNode")
    tmc_helper.compose_sub(assign_json, **ON_OFF_DEVICE_COMMAND_DICT)
    LOGGER.info("AssignResources command is invoked successfully")

    # Verify ObsState is IDLE#
    assert telescope_control.is_in_valid_state(DEVICE_OBS_STATE_IDLE_INFO, "obsState")

    # telescope_control = TelescopeControlMid()
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


