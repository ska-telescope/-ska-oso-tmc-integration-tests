import json

import pytest
import tango
from pytest_bdd import given, parsers, scenario, then, when

from tests.conftest import LOGGER
from tests.resources.test_support.common_utils.result_code import ResultCode
from tests.resources.test_support.common_utils.tmc_helpers import (
    TmcHelper,
    tear_down,
)
from tests.resources.test_support.constant_low import (
    DEVICE_OBS_STATE_EMPTY_INFO,
    DEVICE_OBS_STATE_IDLE_INFO,
    DEVICE_OBS_STATE_READY_INFO,
    DEVICE_STATE_ON_INFO,
    DEVICE_STATE_STANDBY_INFO,
    ON_OFF_DEVICE_COMMAND_DICT,
    centralnode,
    tmc_subarraynode1,
)
from tests.resources.test_support.low.telescope_controls_low import (
    TelescopeControlLow,
)

tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)
telescope_control = TelescopeControlLow()


@pytest.mark.SKA_low
@scenario(
    "../features/check_invalid_json_not_allowed.feature",
    "Invalid json rejected by TMC Low for Configure command",
)
def test_invalid_json_in_configure_obsState():
    """
    Test invalid json in SubarrayNode obsState. CONFIGURE
    """


@given("the TMC is On")
def given_tmc(json_factory):
    release_json = json_factory("command_release_resource_low")
    try:
        # Verify Telescope is Off/Standby
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )

        LOGGER.info("Starting up the Telescope")

        # Invoke TelescopeOn() command on TMC CentralNode
        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
        tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify State transitions after TelescopeOn
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_ON_INFO, "State"
        )

    except Exception:
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)


@given("the subarray is in IDLE obsState")
def tmc_check_status(json_factory):
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
    )
    assign_json = json_factory("command_assign_resource_low")
    LOGGER.info("Invoking AssignResources command on TMC CentralNode")
    tmc_helper.compose_sub(assign_json, **ON_OFF_DEVICE_COMMAND_DICT)

    # Verify ObsState is IDLE
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_IDLE_INFO, "obsState"
    )


@when(
    parsers.parse("the command Configure is invoked with {invalid_json} input")
)
def send(json_factory, invalid_json):
    tmc_subarraynode = tango.DeviceProxy(tmc_subarraynode1)
    release_json = json_factory("command_release_resource_low")
    try:
        configure_json = json_factory("command_Configure_low")
        if invalid_json == "csp_key_missing":
            invalid_configure_json = json.loads(configure_json)
            del invalid_configure_json["csp"]
            LOGGER.info("Invoking Configure command on TMC SubarrayNode")
            pytest.command_result = tmc_subarraynode.Configure(
                json.dumps(invalid_configure_json)
            )
        elif invalid_json == "sdp_key_missing":
            invalid_configure_json = json.loads(configure_json)
            del invalid_configure_json["sdp"]
            LOGGER.info("Invoking Configure command on TMC SubarrayNode")
            pytest.command_result = tmc_subarraynode.Configure(
                json.dumps(invalid_configure_json)
            )
        elif invalid_json == "tmc_key_missing":
            invalid_configure_json = json.loads(configure_json)
            del invalid_configure_json["tmc"]
            pytest.command_result = tmc_subarraynode.Configure(
                json.dumps(invalid_configure_json)
            )
        elif invalid_json == "scan_duration_key_missing":
            invalid_configure_json = json.loads(configure_json)
            del invalid_configure_json["tmc"]["scan_duration"]
            pytest.command_result = tmc_subarraynode.Configure(
                json.dumps(invalid_configure_json)
            )
        elif invalid_json == "empty_string":
            invalid_configure_json = ""
            pytest.command_result = tmc_subarraynode.Configure(
                invalid_configure_json
            )
    except Exception as e:
        LOGGER.exception(f"Exception occurred: {e}")
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)


@then(
    parsers.parse(
        "the TMC should reject the {invalid_json} with ResultCode.Rejected"
    )
)
def invalid_command_rejection(invalid_json):
    # asserting validation resultcode
    assert pytest.command_result[0][0] == ResultCode.REJECTED
    # asserting validations message as per invalid json
    if invalid_json == "csp_key_missing":
        assert (
            "Missing csp key in the scan configuration."
            in pytest.command_result[1][0]
        )
    elif invalid_json == "sdp_key_missing":
        assert (
            "Missing sdp key in the scan configuration."
            in pytest.command_result[1][0]
        )
    elif invalid_json == "tmc_key_missing":
        assert (
            "Missing tmc key in the scan configuration."
            in pytest.command_result[1][0]
        )
    elif invalid_json == "scan_duration_key_missing":
        assert (
            "Missing scan_duration in the scan configuration."
            in pytest.command_result[1][0]
        )
    elif invalid_json == "empty_string":
        assert "Malformed input JSON" in pytest.command_result[1][0]


@then("TMC subarray remains in IDLE obsState")
def tmc_status():
    # Verify obsState transitions
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_IDLE_INFO, "obsState"
    )


@then(
    "TMC successfully executes the Configure \
command for the subarray with a valid json"
)
def tmc_accepts_next_commands(json_factory):
    release_json = json_factory("command_release_resource_low")
    try:
        configure_json = json_factory("command_Configure_low")
        LOGGER.info(f"Input argin for Configure: {configure_json}")

        # Invoke Configure() Command on TMC
        LOGGER.info("Invoking Configure command on TMC SubarrayNode")
        tmc_helper.configure_subarray(
            configure_json, **ON_OFF_DEVICE_COMMAND_DICT
        )
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_READY_INFO, "obsState"
        )

        # teardown
        LOGGER.info("Invoking END on TMC")
        tmc_helper.end(**ON_OFF_DEVICE_COMMAND_DICT)

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

        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )
        LOGGER.info("Tear Down complete. Telescope is in Standby State")
    except Exception:
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)
