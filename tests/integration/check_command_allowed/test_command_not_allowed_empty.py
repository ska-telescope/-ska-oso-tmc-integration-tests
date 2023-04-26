import pytest
from pytest_bdd import given, parsers, scenario, then, when

from tests.conftest import LOGGER
from tests.resources.test_support.common_utils.tmc_helpers import TmcHelper
from tests.resources.test_support.constant import (
    DEVICE_OBS_STATE_EMPTY_INFO,
    DEVICE_OBS_STATE_IDLE_INFO,
    DEVICE_STATE_ON_INFO,
    ON_OFF_DEVICE_COMMAND_DICT,
    centralnode,
    tmc_subarraynode1,
)
from tests.resources.test_support.controls import telescope_is_in_standby_state
from tests.resources.test_support.mid.telescope_controls_mid import (
    TelescopeControlMid,
)
from tests.resources.test_support.tmc_helpers import tear_down

configure_resources_file = "command_Configure.json"
assign_resources_file = "command_AssignResources.json"


tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)
telescope_control = TelescopeControlMid()

@pytest.mark.SKA_mid
@scenario(
    "../features/check_command_not_allowed.feature",
    "Unexpected commands not allowed when TMC subarray is empty",
)
def test_command_not_valid_in_empty_obsState():
    """
    Test commands not allowed in SubarrayNode obsState.EMPTY

    """


@given("the TMC is in ON state and the subarray is in EMPTY obsstate")
def given_tmc():
    # Verify Telescope is Off/Standby
    assert telescope_is_in_standby_state()
    LOGGER.info("Starting up the Telescope")

    # Invoke TelescopeOn() command on TMC CentralNode
    LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
    tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)
    LOGGER.info("TelescopeOn command is invoked successfully")

    # Verify State transitions after TelescopeOn
    assert telescope_control.is_in_valid_state(DEVICE_STATE_ON_INFO, "State")
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
    )


@when(
    parsers.parse(
        "the command {unexpected_command} is invoked on that subarray"
    )
)
def send(json_factory, unexpected_command):
    scan_json = json_factory("command_Scan")
    configure_json = json_factory("command_Configure")
    try:
        if unexpected_command == "Configure":
            LOGGER.info("Invoking Configure command on TMC SubarrayNode")
            tmc_helper.configure_subarray(
                configure_json, **ON_OFF_DEVICE_COMMAND_DICT
            )
        elif unexpected_command == "Scan":
            LOGGER.info("Invoking Scan command on TMC SubarrayNode")
            tmc_helper.scan(scan_json, **ON_OFF_DEVICE_COMMAND_DICT)
        elif unexpected_command == "End":
            LOGGER.info("Invoking End command on TMC SubarrayNode")
            tmc_helper.end()
        elif unexpected_command == "Abort":
            LOGGER.info("Invoking Abort command on TMC SubarrayNode")
            tmc_helper.invoke_abort(**ON_OFF_DEVICE_COMMAND_DICT)
    except Exception as e:
        LOGGER.info(f"Exception occured: {e}")


# TODO: Current version of TMC does not support ResultCode.REJECTED,
# once the implementation is introduced, below block will be updated.
@then(
    parsers.parse(
        "the TMC should reject the {unexpected_command} with ResultCode.Rejected"
    )
)
def invalid_command_rejection(unexpected_command):
    pass


@then("TMC subarray remains in EMPTY obsstate")
def tmc_status():
    # Verify obsState transitions
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
    )


@then("TMC executes the AssignResources command successfully")
def tmc_accepts_next_commands(json_factory):
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")

    # Invoke AssignResources() Command on TMC
    LOGGER.info("Invoking AssignResources command on TMC CentralNode")
    tmc_helper.compose_sub(assign_json, **ON_OFF_DEVICE_COMMAND_DICT)
    LOGGER.info("AssignResources command is invoked successfully")

    # Verify obsState is IDLE
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_IDLE_INFO, "obsState"
    )

    # tear down
    tear_down(release_json)
