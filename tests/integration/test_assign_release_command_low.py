from copy import deepcopy

import pytest
from ska_tango_testing.mock.placeholders import Anything
from tango import DeviceProxy, EventType

from tests.conftest import LOGGER
from tests.resources.test_support.common_utils.result_code import ResultCode
from tests.resources.test_support.common_utils.telescope_controls import (
    BaseTelescopeControl,
)
from tests.resources.test_support.common_utils.tmc_helpers import TmcHelper
from tests.resources.test_support.constant_low import (
    DEVICE_HEALTH_STATE_OK_INFO,
    DEVICE_LIST_FOR_CHECK_DEVICES,
    DEVICE_OBS_STATE_ABORT_INFO,
    DEVICE_OBS_STATE_EMPTY_INFO,
    DEVICE_OBS_STATE_IDLE_INFO,
    DEVICE_STATE_ON_INFO,
    DEVICE_STATE_STANDBY_INFO,
    ON_OFF_DEVICE_COMMAND_DICT,
    centralnode,
    csp_subarray1,
    sdp_subarray1,
    tmc_subarraynode1,
)


# TODO:Create generic one tear down which can be utilized for both low and mid.
def tear_down_for_resourcing(tmc_helper, telescope_control):

    LOGGER.info("Invoking Abort on TMC")

    tmc_helper.invoke_abort(**ON_OFF_DEVICE_COMMAND_DICT)
    LOGGER.info("Invoking Abort command on TMC SubarrayNode")
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_ABORT_INFO, "obsState"
    )

    tmc_helper.invoke_restart(**ON_OFF_DEVICE_COMMAND_DICT)
    LOGGER.info("Invoking Restart command on TMC SubarrayNode")
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
    )

    tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)
    LOGGER.info("Invoking Standby command on TMC SubarrayNode")
    assert telescope_control.is_in_valid_state(
        DEVICE_STATE_STANDBY_INFO, "State"
    )

    LOGGER.info("Tear Down complete. Telescope is in Standby State")


telescope_control = BaseTelescopeControl()
tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)


@pytest.mark.SKA_low
def test_assign_release_low(json_factory):
    """AssignResources and ReleaseResources is executed."""
    assign_json = json_factory("command_assign_resource_low")
    release_json = json_factory("command_release_resource_low")
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

        # Check Telescope availability
        tmc_helper.check_telescope_availability()
        # Invoke Standby() command on TMC
        tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )
    except Exception as e:
        LOGGER.exception("The exception is: %s", e)
        tear_down_for_resourcing(tmc_helper, telescope_control)


@pytest.mark.SKA_low
def test_assign_release_timeout_csp(json_factory, change_event_callbacks):
    """Verify timeout exception raised when csp set to defective."""
    assign_json = json_factory("command_assign_resource_low")
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

        assertion_data = change_event_callbacks[
            "longRunningCommandResult"
        ].assert_change_event(
            (unique_id[0], Anything),
            lookahead=7,
        )
        assert "AssignResources" in assertion_data["attribute_value"][0]
        assert (
            "Exception occurred on the following devices:\n"
            "ska_low/tm_leaf_node/csp_subarray01"
            in assertion_data["attribute_value"][1]
        )
        csp_subarray.SetDefective(False)

        tear_down_for_resourcing(tmc_helper, telescope_control)

    except Exception as e:
        LOGGER.info("In tear down. \nThe Exception is %s", e)
        tear_down_for_resourcing(tmc_helper, telescope_control)


@pytest.mark.SKA_low
def test_assign_release_timeout_sdp(json_factory, change_event_callbacks):
    """Verify timeout exception raised when sdp set to defective."""
    assign_json = json_factory("command_assign_resource_low")
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

        assertion_data = change_event_callbacks[
            "longRunningCommandResult"
        ].assert_change_event(
            (unique_id[0], Anything),
            lookahead=7,
        )
        assert "AssignResources" in assertion_data["attribute_value"][0]
        assert (
            "Exception occurred on the following devices:\n"
            "ska_low/tm_leaf_node/sdp_subarray01"
            in assertion_data["attribute_value"][1]
        )
        sdp_subarray.SetDefective(False)

        tear_down_for_resourcing(tmc_helper, telescope_control)

    except Exception as e:
        LOGGER.info("In tear down. \nThe Exception is %s", e)
        tear_down_for_resourcing(tmc_helper, telescope_control)


@pytest.mark.skip(
    reason="will be enabled when new tag of \
        SDP Subarray Leaf Node will release"
)
@pytest.mark.SKA_low
def test_health_check_low():
    assert telescope_control.is_in_valid_state(
        DEVICE_HEALTH_STATE_OK_INFO, "healthState"
    )
