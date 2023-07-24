from copy import deepcopy

import pytest
from ska_tango_testing.mock.placeholders import Anything
from tango import DeviceProxy, EventType

from tests.conftest import LOGGER
from tests.integration.test_assign_release_command_low import (
    tear_down_for_resourcing,
)
from tests.resources.test_support.common_utils.result_code import ResultCode
from tests.resources.test_support.common_utils.telescope_controls import (
    BaseTelescopeControl,
)
from tests.resources.test_support.common_utils.tmc_helpers import TmcHelper
from tests.resources.test_support.constant_low import (
    DEVICE_STATE_ON_INFO,
    DEVICE_STATE_STANDBY_INFO,
    ON_OFF_DEVICE_COMMAND_DICT,
    centralnode,
    csp_subarray1,
    sdp_subarray1,
    tmc_subarraynode1,
)

telescope_control = BaseTelescopeControl()
tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)


@pytest.mark.test1
@pytest.mark.SKA_low
def test_assign_release_command_not_allowed_propagation_csp_ln_low(
    json_factory, change_event_callbacks
):
    """Verify command not allowed exception propagation from leaf nodes"""
    global tmc_helper, telescope_control
    assign_json = json_factory("command_assign_resource_low")
    try:
        telescope_control = BaseTelescopeControl()
        tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)

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
        # Setting CSP Subarray ObsState to RESOURCING to imulate failure.
        csp_subarray.SetDirectObsState(1)

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
            "ska_tmc_common.exceptions.InvalidObsStateError"
            in assertion_data["attribute_value"][1]
        )

    except Exception as e:
        LOGGER.info(f"Exception occurred {e}")
        tear_down_for_resourcing(tmc_helper, telescope_control)


@pytest.mark.SKA_low
def test_assign_release_command_not_allowed_propagation_sdp_ln_low(
    json_factory, change_event_callbacks
):
    """Verify command not allowed exception propagation from leaf nodes"""
    global telescope_control, tmc_helper
    assign_json = json_factory("command_assign_resource_low")
    try:
        telescope_control = BaseTelescopeControl()
        tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)

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
        # Setting SDP Subarray ObsState to RESOURCING to imulate failure.
        sdp_subarray.SetDirectObsState(1)

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
            lookahead=5,
        )
        assert "AssignResources" in assertion_data["attribute_value"][0]
        assert (
            "ska_tmc_common.exceptions.InvalidObsStateError"
            in assertion_data["attribute_value"][1]
        )
        # Do not raise exception
        tear_down_for_resourcing(tmc_helper, telescope_control)

    except Exception as e:
        LOGGER.info(f"Exception occurred {e}")
        tear_down_for_resourcing(tmc_helper, telescope_control)
