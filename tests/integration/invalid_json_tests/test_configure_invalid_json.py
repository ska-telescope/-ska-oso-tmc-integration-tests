import pytest
from pytest_bdd import given, parsers, scenario, then, when

from tests.conftest import LOGGER
from tests.resources.test_support.common_utils.result_code import ResultCode
from tests.resources.test_support.common_utils.tmc_helpers import TmcHelper
from tests.resources.test_support.constant import (
    DEVICE_OBS_STATE_EMPTY_INFO,
    DEVICE_OBS_STATE_IDLE_INFO,
    DEVICE_OBS_STATE_READY_INFO,
    DEVICE_STATE_ON_INFO,
    ON_OFF_DEVICE_COMMAND_DICT,
    centralnode,
    tmc_subarraynode1,
)
from tests.resources.test_support.controls import telescope_is_in_standby_state
from tests.resources.test_support.telescope_controls import (
    BaseTelescopeControl,
)

configure_resources_file = "command_Configure.json"
assign_resources_file = "command_AssignResources.json"

tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)
telescope_control = BaseTelescopeControl()
result_code = []
message = []


@pytest.mark.xfail(reason="This functionality is not implemented yet in TMC")
@pytest.mark.SKA_mid
@scenario(
    "../features/check_invalid_json_not_allowed.feature",
    "Invalid json rejected by TMC for Configure command",
)
def test_invalid_json_in_configure_obsState():
    """
    Test invalid json in SubarrayNode obsState. CONFIGURE
    """


@given("the TMC is On")
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


@given("the subarray is in IDLE obsState")
def tmc_check_status(json_factory):
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
    )
    assign_json = json_factory("command_AssignResources")
    LOGGER.info("Invoking AssignResources command on TMC CentralNode")
    tmc_helper.compose_sub(assign_json, **ON_OFF_DEVICE_COMMAND_DICT)
    LOGGER.info("AssignResources command is invoked successfully")

    # Verify ObsState is IDLE
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_IDLE_INFO, "obsState"
    )


@when(
    parsers.parse("the command Configure is invoked with {invalid_json} input")
)
def send(json_factory, invalid_json):
    invalid_configure_json = json_factory(invalid_json)
    LOGGER.info("Invoking Configure command on TMC SubarrayNode")
    result, msg = tmc_helper.configure_subarray(
        invalid_configure_json, **ON_OFF_DEVICE_COMMAND_DICT
    )
    result_code.append(result)
    message.append(msg)


# once the implementation is introduced, below block will be updated.
@then(
    parsers.parse(
        "the TMC should reject the {invalid_json} with ResultCode.Rejected"
    )
)
def invalid_command_rejection():
    # validation msg assert invalid_command_rejection(result_code, message)
    LOGGER.info(f"Asserting {result_code} ")
    assert result_code[0] == ResultCode.REJECTED


# TODO: Current version of TMC - subarray is remaining in Configuring
@then("TMC subarray remains in IDLE obsState")
def tmc_status():
    # Verify obsState transitions
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_IDLE_INFO, "obsState"
    )


@then(
    "TMC successfully executes the Configure\
          command for the subarray with a valid json"
)
def tmc_accepts_next_commands(json_factory):
    configure_json = json_factory("command_Configure")
    release_json = json_factory("command_ReleaseResources")
    # Invoke AssignResources() Command on TMC
    LOGGER.info("Invoking Configure command on TMC SubarrayNode")
    tmc_helper.configure_subarray(configure_json, **ON_OFF_DEVICE_COMMAND_DICT)
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_READY_INFO, "obsState"
    )

    # teardown
    LOGGER.info("Invoking END on TMC")
    tmc_helper.end()

    #  Verify obsState is IDLE
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_IDLE_INFO, "obsState"
    )

    LOGGER.info("Invoking ReleaseResources on TMC")
    tmc_helper.invoke_releaseResources(
        release_json, **ON_OFF_DEVICE_COMMAND_DICT
    )

    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
    )

    LOGGER.info("Invoking Telescope Standby on TMC")
    tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)

    assert telescope_is_in_standby_state()
    LOGGER.info("Tear Down complete. Telescope is in Standby State")
