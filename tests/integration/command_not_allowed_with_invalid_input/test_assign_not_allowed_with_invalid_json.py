import json

import pytest
from pytest_bdd import given, parsers, scenario, then, when

from tests.conftest import LOGGER
from tests.resources.test_support.common_utils.result_code import ResultCode
from tests.resources.test_support.common_utils.tmc_helpers import TmcHelper
from tests.resources.test_support.constant import (
    DEVICE_OBS_STATE_EMPTY_INFO,
    DEVICE_OBS_STATE_IDLE_INFO,
    DEVICE_STATE_ON_INFO,
    DEVICE_STATE_STANDBY_INFO,
    ON_OFF_DEVICE_COMMAND_DICT,
    centralnode,
    tmc_subarraynode1,
)
from tests.resources.test_support.telescope_controls import (
    BaseTelescopeControl,
)
from tests.resources.test_support.tmc_helpers import tear_down

tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)
telescope_control = BaseTelescopeControl()


@pytest.mark.xfail(reason="This functionality is not implemented yet in TMC")
@pytest.mark.SKA_mid
@scenario(
    "../features/invalid_json_not_allowed.feature",
    "AssignResource command with invalid JSON is rejected by the TMC",
)
def test_assign_resource_with_invalid_json():
    """
    Test AssignResource command with input as invalid json.

    """


@given("the TMC is in ON state")
def given_tmc():
    # Verify Telescope is Off/Standby
    assert telescope_control.is_in_valid_state(
        DEVICE_STATE_STANDBY_INFO, "State"
    )
    # Invoke TelescopeOn() command on TMC CentralNode
    LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
    tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)
    LOGGER.info("TelescopeOn command is invoked successfully")
    # Verify State transitions after TelescopeOn
    assert telescope_control.is_in_valid_state(DEVICE_STATE_ON_INFO, "State")


@given("the subarray is in EMPTY obsState")
def given_tmc_obsstate():
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
    )


@when(
    parsers.parse(
        "the command AssignResources is invoked with {invalid_json} input"
    )
)
def send(json_factory, invalid_json):
    try:
        assign_invalid_json = json_factory("command_AssignResources")
        release_json = json_factory("command_ReleaseResources")
        assign_invalid_json = json.loads(assign_invalid_json)
        if invalid_json == "pb_id":
            del assign_invalid_json["sdp"]["processing_blocks"][0]["pb_id"]
            # Invoke AssignResources() Command on TMC
            LOGGER.info("Invoking AssignResources command on TMC CentralNode")
            pytest.command_result = tmc_helper.compose_sub(
                json.dumps(assign_invalid_json), **ON_OFF_DEVICE_COMMAND_DICT
            )
        elif invalid_json == "scan_type_id":
            del assign_invalid_json["sdp"]["execution_block"]["scan_types"][0][
                "scan_type_id"
            ]
            # Invoke AssignResources() Command on TMC
            LOGGER.info("Invoking AssignResources command on TMC CentralNode")
            pytest.command_result = tmc_helper.compose_sub(
                json.dumps(assign_invalid_json), **ON_OFF_DEVICE_COMMAND_DICT
            )
        elif invalid_json == "count":
            del assign_invalid_json["sdp"]["execution_block"]["channels"][0][
                "channels_id"
            ]
            # Invoke AssignResources() Command on TMC
            LOGGER.info("Invoking AssignResources command on TMC CentralNode")
            pytest.command_result = tmc_helper.compose_sub(
                json.dumps(assign_invalid_json), **ON_OFF_DEVICE_COMMAND_DICT
            )
        elif invalid_json == "receptor_id ":
            del assign_invalid_json["dish"]["receptor_id"]
            # Invoke AssignResources() Command on TMC
            LOGGER.info("Invoking AssignResources command on TMC CentralNode")
            pytest.command_result = tmc_helper.compose_sub(
                json.dumps(assign_invalid_json), **ON_OFF_DEVICE_COMMAND_DICT
            )

    except Exception as e:
        LOGGER.exception(f"Exception occured: {e}")
        tear_down(release_json)


# TODO: Current version of TMC does not support ResultCode.REJECTED,
# once the implementation is introduced, below block will be updated.
@then(parsers.parse("TMC should reject the AssignResources command"))
def invalid_command_rejection():
    assert (
        (
            """JSON validation error: data is not compliant with \
            https://schema.skao.int/ska-tmc-assignresources"""
        )
        in pytest.command_result[1][0]
    )

    assert pytest.command_result[0][0] == ResultCode.REJECTED
    pass


@then("TMC subarray remains in EMPTY obsState")
def tmc_status():
    # Verify obsState transitions
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
    )


@then("the command AssignResources is invoked with valid_json input")
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

        # tear down
        tmc_helper.invoke_releaseResources(
            release_json, **ON_OFF_DEVICE_COMMAND_DICT
        )
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
        )
        tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )
        LOGGER.info("Tests complete.")
    except Exception:
        tear_down(release_json)
