import pytest
from pytest_bdd import given, parsers, scenario, then, when

from tests.conftest import LOGGER
from tests.resources.test_support.common_utils.result_code import ResultCode
from tests.resources.test_support.common_utils.telescope_controls import (
    BaseTelescopeControl,
)
from tests.resources.test_support.common_utils.tmc_helpers import TmcHelper
from tests.resources.test_support.constant import (
    DEVICE_LIST_FOR_CHECK_DEVICES,
    DEVICE_OBS_STATE_EMPTY_INFO,
    DEVICE_OBS_STATE_IDLE_INFO,
    DEVICE_STATE_ON_INFO,
    DEVICE_STATE_STANDBY_INFO,
    ON_OFF_DEVICE_COMMAND_DICT,
    centralnode,
    tmc_subarraynode1,
)

configure_resources_file = "command_Configure.json"
assign_resources_file = "command_AssignResources.json"


tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)
telescope_control = BaseTelescopeControl()
result, message = "", ""


@pytest.mark.xfail(reason="This functionality is not implemented yet in TMC")
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
    tmc_helper.check_devices(DEVICE_LIST_FOR_CHECK_DEVICES)
    assert telescope_control.is_in_valid_state(
        DEVICE_STATE_STANDBY_INFO, "State"
    )
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
            result, message = tmc_helper.configure_subarray(
                configure_json, **ON_OFF_DEVICE_COMMAND_DICT
            )
        elif unexpected_command == "Scan":
            LOGGER.info("Invoking Scan command on TMC SubarrayNode")
            result, message = tmc_helper.scan(
                scan_json, **ON_OFF_DEVICE_COMMAND_DICT
            )
        elif unexpected_command == "End":
            LOGGER.info("Invoking End command on TMC SubarrayNode")
            result, message = tmc_helper.end()
        elif unexpected_command == "Abort":
            LOGGER.info("Invoking Abort command on TMC SubarrayNode")
            result, message = tmc_helper.invoke_abort(
                **ON_OFF_DEVICE_COMMAND_DICT
            )
    except Exception as e:
        LOGGER.info(f"Exception occured: {e}")


@then(
    parsers.parse(
        "TMC should reject the {unexpected_command} with ResultCode.Rejected"
    )
)
def invalid_command_rejection(unexpected_command):
    assert (
        f"command {unexpected_command} is not allowed \
        in current subarray obsState"
        in message[0]
    )
    assert result[0] == ResultCode.REJECTED


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
    LOGGER.info("Invoking ReleaseResources command on TMC SubarrayNode")
    tmc_helper.invoke_releaseResources(
        release_json, **ON_OFF_DEVICE_COMMAND_DICT
    )
    assert telescope_control.is_in_valid_state(DEVICE_STATE_ON_INFO, "State")
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
    )

    LOGGER.info("Invoking Standby command on TMC SubarrayNode")
    tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)
    assert telescope_control.is_in_valid_state(
        DEVICE_STATE_STANDBY_INFO, "State"
    )

    LOGGER.info("Tear Down complete. Telescope is in Standby State")
