"""Test cases for Configure and End Command
    for mid"""
import json
from copy import deepcopy

import pytest
from ska_tango_testing.mock.placeholders import Anything
from tango import DeviceProxy, EventType

from tests.conftest import LOGGER
from tests.resources.test_support.common_utils.result_code import ResultCode
from tests.resources.test_support.common_utils.telescope_controls import (
    BaseTelescopeControl,
    check_subarray1_availability,
)
from tests.resources.test_support.common_utils.tmc_helpers import (
    TmcHelper,
    tear_down,
)
from tests.resources.test_support.constant import (
    COMMAND_NOT_ALLOWED_DEFECT,
    DEVICE_LIST_FOR_CHECK_DEVICES,
    DEVICE_OBS_STATE_EMPTY_INFO,
    DEVICE_OBS_STATE_IDLE_INFO,
    DEVICE_OBS_STATE_READY_INFO,
    DEVICE_STATE_ON_INFO,
    DEVICE_STATE_STANDBY_INFO,
    INTERMEDIATE_STATE_DEFECT,
    ON_OFF_DEVICE_COMMAND_DICT,
    centralnode,
    csp_subarray1,
    sdp_subarray1,
    tmc_csp_subarray_leaf_node,
    tmc_sdp_subarray_leaf_node,
    tmc_subarraynode1,
)

tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)
telescope_control = BaseTelescopeControl()


@pytest.mark.skip(reason="Random failure due to old configure id.")
@pytest.mark.SKA_mid
def test_configure_end(json_factory):
    """Configure and End is executed."""
    release_json = json_factory("command_ReleaseResources")
    assign_json = json_factory("command_AssignResources")
    configure_json = json_factory("command_Configure")
    try:
        # Verify Telescope is Off/Standby
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

        # Check Subarray1 availability
        assert check_subarray1_availability(tmc_subarraynode1)

        # Invoke AssignResources() Command on TMC
        tmc_helper.compose_sub(assign_json, **ON_OFF_DEVICE_COMMAND_DICT)
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_IDLE_INFO, "obsState"
        )

        # Invoke Configure() Command on TMC
        tmc_helper.configure_subarray(
            configure_json, **ON_OFF_DEVICE_COMMAND_DICT
        )
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_READY_INFO, "obsState"
        )
        # Teardowning
        # Invoke End() Command on TMC
        tmc_helper.end(**ON_OFF_DEVICE_COMMAND_DICT)
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
def test_configure_timeout_and_error_propagation_csp(
    json_factory, change_event_callbacks
):
    """Verify timeout exception raised when csp set to defective."""
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")
    configure_json = json_factory("command_Configure")
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
        tmc_helper.compose_sub(assign_json, **ON_OFF_DEVICE_COMMAND_DICT)

        # Verify transitions after AssignResources command
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_IDLE_INFO, "obsState"
        )

        subarray_node_proxy = DeviceProxy(tmc_subarraynode1)
        subarray_node_proxy.subscribe_event(
            "longRunningCommandResult",
            EventType.CHANGE_EVENT,
            change_event_callbacks["longRunningCommandResult"],
        )

        csp_subarray = DeviceProxy(csp_subarray1)
        csp_subarray.SetDefective(json.dumps(INTERMEDIATE_STATE_DEFECT))

        # Invoking Configure command
        device_params = deepcopy(ON_OFF_DEVICE_COMMAND_DICT)
        device_params["set_wait_for_obsstate"] = False
        result_code, unique_id = tmc_helper.configure_subarray(
            configure_json, **device_params
        )
        assert unique_id[0].endswith("Configure")
        assert result_code[0] == ResultCode.QUEUED

        assertion_data = change_event_callbacks[
            "longRunningCommandResult"
        ].assert_change_event(
            (unique_id[0], Anything),
            lookahead=7,
        )

        assert "Configure" in assertion_data["attribute_value"][0]
        assert (
            "Timeout has occurred, command failed"
            in assertion_data["attribute_value"][1]
        )
        assert (
            tmc_csp_subarray_leaf_node in assertion_data["attribute_value"][1]
        )

        change_event_callbacks["longRunningCommandResult"].assert_change_event(
            (unique_id[0], str(ResultCode.FAILED.value)),
            lookahead=4,
        )

        csp_subarray.SetDefective(json.dumps({"enabled": False}))

        tear_down(
            release_json, raise_exception=False, **ON_OFF_DEVICE_COMMAND_DICT
        )

    except Exception as e:
        LOGGER.exception("The exception is: %s", e)
        tear_down(
            release_json, raise_exception=True, **ON_OFF_DEVICE_COMMAND_DICT
        )


@pytest.mark.skip(reason="Need to update the way to induce fault on SDP SA")
@pytest.mark.SKA_mid
def test_configure_timeout_sdp(json_factory, change_event_callbacks):
    """Verify timeout exception raised when csp set to defective."""
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")
    configure_json = json_factory("command_Configure")
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
        tmc_helper.compose_sub(assign_json, **ON_OFF_DEVICE_COMMAND_DICT)

        # Verify transitions after AssignResources command
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_IDLE_INFO, "obsState"
        )

        subarray_node_proxy = DeviceProxy(tmc_subarraynode1)
        subarray_node_proxy.subscribe_event(
            "longRunningCommandResult",
            EventType.CHANGE_EVENT,
            change_event_callbacks["longRunningCommandResult"],
        )

        sdp_subarray = DeviceProxy(sdp_subarray1)
        sdp_subarray.SetDefective(json.dumps(INTERMEDIATE_STATE_DEFECT))

        # Invoking Configure command
        device_params = deepcopy(ON_OFF_DEVICE_COMMAND_DICT)
        device_params["set_wait_for_obsstate"] = False
        result_code, unique_id = tmc_helper.configure_subarray(
            configure_json, **device_params
        )
        assert unique_id[0].endswith("Configure")
        assert result_code[0] == ResultCode.QUEUED

        assertion_data = change_event_callbacks[
            "longRunningCommandResult"
        ].assert_change_event(
            (unique_id[0], Anything),
            lookahead=7,
        )

        assert "Configure" in assertion_data["attribute_value"][0]
        assert (
            "Timeout has occurred, command failed"
            in assertion_data["attribute_value"][1]
        )
        assert (
            tmc_sdp_subarray_leaf_node in assertion_data["attribute_value"][1]
        )

        change_event_callbacks["longRunningCommandResult"].assert_change_event(
            (unique_id[0], str(ResultCode.FAILED.value)),
            lookahead=4,
        )

        sdp_subarray.SetDefective(json.dumps({"enabled": False}))

        tear_down(
            release_json, raise_exception=False, **ON_OFF_DEVICE_COMMAND_DICT
        )

    except Exception as e:
        LOGGER.exception("The exception is: %s", e)
        tear_down(
            release_json, raise_exception=True, **ON_OFF_DEVICE_COMMAND_DICT
        )


@pytest.mark.SKA_mid
def test_configure_error_propagation_sdp(json_factory, change_event_callbacks):
    """Verify timeout exception raised when csp set to defective."""
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")
    configure_json = json_factory("command_Configure")
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
        tmc_helper.compose_sub(assign_json, **ON_OFF_DEVICE_COMMAND_DICT)

        # Verify transitions after AssignResources command
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_IDLE_INFO, "obsState"
        )

        subarray_node_proxy = DeviceProxy(tmc_subarraynode1)
        subarray_node_proxy.subscribe_event(
            "longRunningCommandResult",
            EventType.CHANGE_EVENT,
            change_event_callbacks["longRunningCommandResult"],
        )

        sdp_subarray = DeviceProxy(sdp_subarray1)
        sdp_subarray.SetDefective(json.dumps(COMMAND_NOT_ALLOWED_DEFECT))

        # Invoking Configure command
        device_params = deepcopy(ON_OFF_DEVICE_COMMAND_DICT)
        device_params["set_wait_for_obsstate"] = False
        result_code, unique_id = tmc_helper.configure_subarray(
            configure_json, **device_params
        )
        assert unique_id[0].endswith("Configure")
        assert result_code[0] == ResultCode.QUEUED

        assertion_data = change_event_callbacks[
            "longRunningCommandResult"
        ].assert_change_event(
            (unique_id[0], Anything),
            lookahead=7,
        )

        assert "Configure" in assertion_data["attribute_value"][0]
        assert (
            "Exception to test exception propagation"
            in assertion_data["attribute_value"][1]
        )
        assert (
            tmc_sdp_subarray_leaf_node in assertion_data["attribute_value"][1]
        )
        change_event_callbacks["longRunningCommandResult"].assert_change_event(
            (unique_id[0], str(ResultCode.FAILED.value)),
            lookahead=4,
        )
        sdp_subarray.SetDefective(json.dumps({"enabled": False}))
        tear_down(
            release_json, raise_exception=False, **ON_OFF_DEVICE_COMMAND_DICT
        )

    except Exception as e:
        LOGGER.exception("The exception is: %s", e)
        tear_down(
            release_json, raise_exception=True, **ON_OFF_DEVICE_COMMAND_DICT
        )
