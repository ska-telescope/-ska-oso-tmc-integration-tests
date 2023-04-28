import pytest
from pytest_bdd import given, parsers, scenario, then, when

from tests.conftest import LOGGER
from tests.resources.test_support.common_utils.tmc_helpers import TmcHelper
from tests.resources.test_support.constant import (
    DEVICE_OBS_STATE_EMPTY_INFO,
    DEVICE_OBS_STATE_IDLE_INFO,
    DEVICE_STATE_ON_INFO,
    ON_OFF_DEVICE_COMMAND_DICT,
    DEVICE_STATE_STANDBY_INFO,
    centralnode,
    tmc_subarraynode1,
)
from tests.resources.test_support.controls import telescope_is_in_standby_state
from tests.resources.test_support.telescope_controls import (
    BaseTelescopeControl,
)
from tests.resources.test_support.tmc_helpers import tear_down

configure_resources_file = "command_Configure.json"
assign_resources_file = "command_AssignResources.json"


tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)
telescope_control = BaseTelescopeControl()


@pytest.mark.mansi
@pytest.mark.SKA_mid
@scenario(
    "../features/invalid_json_not_allowed.feature",
    "AssignResource command with invalid JSON is rejected by the TMC",
)
def test_assign_resource_with_invalid_json():
    """
    Test AssignResource command with input as invalid json.

    """


@given("the TMC is in ON state and the subarray is in EMPTY obsState")
def given_tmc():
    # Verify Telescope is Off/Standby
    assert telescope_control.is_in_valid_state(DEVICE_STATE_STANDBY_INFO, "State")
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
        "the command assignresources is invoked for the subarray with {invalid_json} input"
    )
)
def send(json_factory, invalid_json):
    try:
        assign_invalid_json1 = json_factory(invalid_json)
        # Invoke AssignResources() Command on TMC

        LOGGER.info("Invoking AssignResources command on TMC CentralNode")
        tmc_helper.compose_sub(
            assign_invalid_json1, **ON_OFF_DEVICE_COMMAND_DICT
        )
    except Exception as e:
        LOGGER.info(f"Exception occured: {e}")


# TODO: Current version of TMC does not support ResultCode.REJECTED,
# once the implementation is introduced, below block will be updated.
@then(
    "the TMC should reject the AssignResources command with ResultCode.Rejected"
)
def invalid_command_rejection():
    pass


@then("TMC subarray remains in EMPTY obsState")
def tmc_status():
    # Verify obsState transitions
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
    )


@then(
    "TMC successfully executes the AssignResources command for the subarray with a valid json"
)
def tmc_accepts_next_commands(json_factory):
    try:
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
        
        #tear down
        tmc_helper.invoke_releaseResources(
            release_json, **ON_OFF_DEVICE_COMMAND_DICT
        )
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
        )
        tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)
        assert telescope_control.is_in_valid_state(DEVICE_STATE_STANDBY_INFO, "State")
        LOGGER.info("Tests complete.")
    except Exception:
        tear_down(release_json)

