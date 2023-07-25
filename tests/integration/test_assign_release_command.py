"""test cases for assign_release resources command for mid"""
import json
from copy import deepcopy

import pytest
from tango import DeviceProxy, EventType

from tests.conftest import LOGGER
from tests.resources.test_support.common_utils.result_code import ResultCode
from tests.resources.test_support.common_utils.telescope_controls import (
    BaseTelescopeControl,
)
from tests.resources.test_support.common_utils.tmc_helpers import (
    TmcHelper,
    tear_down,
)
from tests.resources.test_support.constant import (
    DEVICE_HEALTH_STATE_OK_INFO,
    DEVICE_LIST_FOR_CHECK_DEVICES,
    DEVICE_OBS_STATE_EMPTY_INFO,
    DEVICE_OBS_STATE_IDLE_INFO,
    DEVICE_STATE_ON_INFO,
    DEVICE_STATE_STANDBY_INFO,
    ON_OFF_DEVICE_COMMAND_DICT,
    centralnode,
    csp_subarray1,
    sdp_subarray1,
    tmc_csp_subarray_leaf_node,
    tmc_sdp_subarray_leaf_node,
    tmc_subarraynode1,
)

telescope_control = BaseTelescopeControl()
tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)


@pytest.mark.SKA_mid
def test_assign_release(json_factory):
    """AssignResources and ReleaseResources is executed."""
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")
    try:
        tmc_helper.check_devices(DEVICE_LIST_FOR_CHECK_DEVICES)
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )
        # Invoke TelescopeOn() command on TMC CentralNode
        tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)
        # Verify State transitions after TelescopeOn
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_ON_INFO, "State"
        )

        # Check Telescope availability
        tmc_helper.check_telescope_availability()
        # Invoke AssignResources() Command on TMC
        tmc_helper.compose_sub(assign_json, **ON_OFF_DEVICE_COMMAND_DICT)
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_IDLE_INFO, "obsState"
        )

        # Invoke ReleaseResources() command on TMC
        tmc_helper.invoke_releaseResources(
            release_json, **ON_OFF_DEVICE_COMMAND_DICT
        )
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
        )

        # Invoke Standby() command on TMC
        tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )
    except Exception as e:
        LOGGER.exception("The exception is: %s", e)
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)


@pytest.mark.SKA_mid
def test_assign_release_with_meerkat_ids(json_factory):
    """AssignResources and ReleaseResources is executed."""
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")
    # Replace SKA dish ids with MeerKAT dish ids
    json_argument = json.loads(assign_json)
    json_argument["dish"]["receptor_ids"] = ["MKT001", "MKT002"]
    json_argument = json.dumps(json_argument)
    try:
        tmc_helper.check_devices(DEVICE_LIST_FOR_CHECK_DEVICES)

        # Verify Telescope is Off/Standby
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )

        # Invoke TelescopeOn() command on TMC
        tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify State transitions after TelescopeOn
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_ON_INFO, "State"
        )

        # Invoke AssignResources() Command on TMC
        tmc_helper.compose_sub(json_argument, **ON_OFF_DEVICE_COMMAND_DICT)

        # Verify ObsState is Idle
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_IDLE_INFO, "obsState"
        )

        # Invoke ReleaseResources() command on TMC
        tmc_helper.invoke_releaseResources(
            release_json, **ON_OFF_DEVICE_COMMAND_DICT
        )

        # Verify ObsState is Empty
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
        )

        # Invoke TelescopeStandby() command on TMC
        tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify State transitions after TelescopeStandby
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )
        LOGGER.info("Tests complete.")

    except Exception as e:
        LOGGER.exception("The exception is: %s", e)
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)


@pytest.mark.skip(
    reason="Abort command is not implemented on SDP Subarray Leaf Node."
)
@pytest.mark.SKA_mid
def test_assign_release_timeout(json_factory, change_event_callbacks):
    """Verify timeout exception raised when csp set to defective."""
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")
    try:
        # Verify Telescope is Off/Standby
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )

        # Invoke TelescopeOn() command on TMC
        tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify State transitions after TelescopeOn
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_ON_INFO, "State"
        )

        # Invoke AssignResources() Command on TMC
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")
        # Verify State transitions after TelescopeOn

        central_node = DeviceProxy(centralnode)
        central_node.subscribe_event(
            "longRunningCommandResult",
            EventType.CHANGE_EVENT,
            change_event_callbacks["longRunningCommandResult"],
        )

        csp_subarray = DeviceProxy(csp_subarray1)
        csp_subarray.SetDefective(True)

        device_params = deepcopy(ON_OFF_DEVICE_COMMAND_DICT)
        device_params["set_wait_for_obsstate"] = False
        result, unique_id = tmc_helper.compose_sub(
            assign_json, **device_params
        )

        LOGGER.info(f"Command result {result} and unique id {unique_id}")

        assert unique_id[0].endswith("AssignResources")
        assert result[0] == ResultCode.QUEUED

        exception_message = (
            f"Exception occured on device: "
            f"{tmc_subarraynode1}: Exception occurred on the following devices"
            f":\n{tmc_csp_subarray_leaf_node}: Timeout has "
            f"occured, command failed\n"
        )

        change_event_callbacks["longRunningCommandResult"].assert_change_event(
            (unique_id[0], exception_message),
            lookahead=9,
        )
        csp_subarray.SetDefective(False)

        # Do not raise exception
        tear_down(
            release_json, raise_exception=False, **ON_OFF_DEVICE_COMMAND_DICT
        )

    except Exception as e:
        LOGGER.exception("The exception is: %s", e)
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)


@pytest.mark.skip(
    reason="Abort command is not implemented on SDP Subarray Leaf Node."
)
@pytest.mark.SKA_mid
def test_assign_release_timeout_sdp(json_factory, change_event_callbacks):
    """Verify timeout exception raised when sdpp set to defective."""
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")
    try:
        # Verify Telescope is Off/Standby
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )

        # Invoke TelescopeOn() command on TMC
        tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify State transitions after TelescopeOn
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_ON_INFO, "State"
        )

        # Invoke AssignResources() Command on TMC
        central_node = DeviceProxy(centralnode)
        central_node.subscribe_event(
            "longRunningCommandResult",
            EventType.CHANGE_EVENT,
            change_event_callbacks["longRunningCommandResult"],
        )

        sdp_subarray = DeviceProxy(sdp_subarray1)
        sdp_subarray.SetDefective(True)

        device_params = deepcopy(ON_OFF_DEVICE_COMMAND_DICT)
        device_params["set_wait_for_obsstate"] = False
        result, unique_id = tmc_helper.compose_sub(
            assign_json, **device_params
        )

        LOGGER.info(f"Command result {result} and unique id {unique_id}")

        assert unique_id[0].endswith("AssignResources")
        assert result[0] == ResultCode.QUEUED

        exception_message = (
            f"Exception occured on device: "
            f"{tmc_subarraynode1}: Exception occurred on the following devices"
            f":\n{tmc_sdp_subarray_leaf_node}: Timeout has "
            f"occured, command failed\n"
        )

        change_event_callbacks["longRunningCommandResult"].assert_change_event(
            (unique_id[0], exception_message),
            lookahead=7,
        )
        sdp_subarray.SetDefective(False)

        # Do not raise exception
        tear_down(
            release_json, raise_exception=False, **ON_OFF_DEVICE_COMMAND_DICT
        )

    except Exception as e:
        LOGGER.exception("The exception is: %s", e)
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)


@pytest.mark.skip(
    reason="will be enabled when new tag of \
        SDP Subarray Leaf Node will release"
)
@pytest.mark.SKA_mid
def test_health_check_mid():
    """test case to check health check for mid"""
    assert telescope_control.is_in_valid_state(
        DEVICE_HEALTH_STATE_OK_INFO, "healthState"
    )
