import json
import time

import pytest
from pytest_bdd import given, scenario, then, when
from tango import DeviceProxy

from tests.conftest import LOGGER
from tests.resources.test_support.common_utils.common_helpers import resource
from tests.resources.test_support.common_utils.result_code import ResultCode
from tests.resources.test_support.common_utils.tmc_helpers import (
    TmcHelper,
    tear_down,
)
from tests.resources.test_support.constant import (
    DEVICE_OBS_STATE_EMPTY_INFO,
    DEVICE_OBS_STATE_IDLE_INFO,
    DEVICE_OBS_STATE_READY_INFO,
    DEVICE_OBS_STATE_SCANNING_INFO,
    DEVICE_STATE_ON_INFO,
    DEVICE_STATE_STANDBY_INFO,
    ON_OFF_DEVICE_COMMAND_DICT,
    centralnode,
    tmc_subarraynode1,
)
from tests.resources.test_support.telescope_controls import (
    BaseTelescopeControl,
)

tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)
telescope_control = BaseTelescopeControl()



@pytest.mark.SKA_mid
@scenario(
    "../features/successful_scan_after_failed_assigned.feature",
    "Successfully execute a scan after a failed attempt to assign resources",
)
def test_assign_resource_with_invalid_json():
    """
    Test AssignResource command with input as invalid json.

    """


@given("a subarray with resources in obsState EMPTY")
def given_tmc(json_factory):
    release_json = json_factory("command_ReleaseResources")
    try:
        # Verify Telescope is Off/Standby
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )
        # Invoke TelescopeOn() command on TMC CentralNode
        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
        tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)
        # Verify State transitions after TelescopeOn
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_ON_INFO, "State"
        )
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
        )
    except Exception:
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)


@when(
    "I issue the command AssignResources passing an invalid JSON script to \
the subarray"
)
def send(
    json_factory,
):
    try:
        assign_json = json_factory("command_AssignResources")
        release_json = json_factory("command_ReleaseResources")
        assign_json = json.loads(assign_json)
        del assign_json["sdp"]["processing_blocks"][0]["pb_id"]
        # Invoke AssignResources() Command on TMC
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")
        central_node = DeviceProxy(centralnode)
        pytest.command_result = central_node.AssignResources(
            json.dumps(assign_json)
        )
    except Exception as e:
        LOGGER.info("The Exception is %s", e)
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)


@then("the subarray returns an error message")
def invalid_command_rejection():
    assert "JSON validation error" in pytest.command_result[1][0]
    assert pytest.command_result[0][0] == ResultCode.REJECTED


@then("the subarray remains in obsState EMPTY")
def tmc_status():
    # Verify obsState transitions
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
    )


@when("I issue the command AssignResources passing a correct JSON script")
def tmc_accepts_command_with_valid_json(json_factory):
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
    except Exception:
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)


@then("the subarray transitions to obsState IDLE")
def tmc_status_idle(json_factory):
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_IDLE_INFO, "obsState"
    )


@when("I issue the command Configure passing a correct JSON script")
def tmc_accepts_configure_command_with_valid_json(json_factory):
    configure_json = json_factory("command_Configure")
    release_json = json_factory("command_ReleaseResources")
    try:
        tmc_helper.configure_subarray(
            configure_json, **ON_OFF_DEVICE_COMMAND_DICT
        )
        LOGGER.info("Invoking Configure command on TMC CentralNode")
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_READY_INFO, "obsState"
        )
    except Exception:
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)
        LOGGER.info("Tear Down complete. Telescope is in Standby State")


@then("the subarray transitions to obsState READY")
def tmc_status_ready():
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_READY_INFO, "obsState"
    )


@when("I issue the command Scan")
def tmc_accepts_scan_command(json_factory):
    scan_json = json_factory("command_Scan")
    release_json = json_factory("command_ReleaseResources")
    try:
        subarray_node = DeviceProxy(tmc_subarraynode1)
        subarray_node.Scan(scan_json)
        time.sleep(1)
        LOGGER.info("Invoking Scan command on TMC Subarray Node")
        resource(tmc_subarraynode1).assert_attribute("obsState").equals(
            "SCANNING"
        )
    except Exception:
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)
        LOGGER.info("Tear Down complete. Telescope is in Standby State")


@then("the subarray transitions to obsState SCANNING")
def tmc_status_scanning(json_factory):
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_SCANNING_INFO, "obsState"
    )


@when("I issue the command EndScan")
def tmc_accepts_endscan_command(json_factory):
    release_json = json_factory("command_ReleaseResources")
    try:
        subarray_node = DeviceProxy(tmc_subarraynode1)
        subarray_node.EndScan()
        LOGGER.info("Invoking EndScan command on TMC SubarrayNode")
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_READY_INFO, "obsState"
        )

    except Exception:
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)
        LOGGER.info("Tear Down complete. Telescope is in Standby State")


# @then("the subarray transitions to obsState READY")


@then("the data is recorded as expected")
def data_recorded_as_expected(json_factory):
    release_json = json_factory("command_ReleaseResources")
    tmc_helper.end(**ON_OFF_DEVICE_COMMAND_DICT)
    LOGGER.info("Invoking End command on TMC SubarrayNode")
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_IDLE_INFO, "obsState"
    )
    tmc_helper.invoke_releaseResources(
        release_json, **ON_OFF_DEVICE_COMMAND_DICT
    )
    LOGGER.info("Invoking ReleaseResources command on TMC SubarrayNode")
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
    )
    tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)
    LOGGER.info("Invoking Standby command on TMC SubarrayNode")
    assert telescope_control.is_in_valid_state(
        DEVICE_STATE_STANDBY_INFO, "State"
    )


@pytest.mark.kk
@pytest.mark.SKA_mid
@scenario(
    "../features/successful_scan_after_failed_assigned.feature",
    "Successfully execute a scan after a successive failed attempt to assign resources",
)
def test_assign_resource_after_successive_assign_failure():
    """
    Test AssignResource command with input as invalid json.

    """