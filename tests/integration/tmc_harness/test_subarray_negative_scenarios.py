"""Implement negative scenario test cases for subarray
"""
import pytest
from ska_tango_base.control_model import ObsState

from tests.resources.test_harness.helpers import (
    device_is_with_correct_command_recorder_data,
    prepare_json_args_for_commands,
)
from tests.resources.test_harness.utils.enums import MockDeviceType


class TestSubarrayNodeNegative(object):
    @pytest.mark.SKA_mid
    def test_subarray_assign_csp_unresponsive(
        self,
        subarray_node,
        command_input_factory,
        mock_factory,
        event_recorder,
    ):
        input_json = prepare_json_args_for_commands(
            "assign_resources_mid", command_input_factory
        )
        csp_mock = mock_factory.get_or_create_mock_device(
            MockDeviceType.CSP_DEVICE
        )
        # Subscribe for long running command result attribute
        # so that error message from subarray can be validated
        event_recorder.subscribe_event(
            subarray_node.subarray_node, "longRunningCommandResult"
        )

        subarray_node.move_to_on()

        subarray_node.force_change_of_obs_state("EMPTY")

        # Set csp defective and execute configure command
        csp_mock.SetDefective(True)

        _, unique_id = subarray_node.execute_transition(
            "AssignResources", argin=input_json
        )

        exception_message = (
            "Exception occured on device"
            ": ska_mid/tm_leaf_node/csp_subarray01: Timeout has "
            "occured, command failed"
        )

        expected_long_running_command_result = (
            unique_id[0],
            exception_message,
        )

        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node,
            "longRunningCommandResult",
            expected_long_running_command_result,
        )

    @pytest.mark.test
    @pytest.mark.SKA_mid
    def test_subarray_configure_csp_unresponsive(
        self,
        subarray_node,
        command_input_factory,
        mock_factory,
        event_recorder,
    ):
        input_json = prepare_json_args_for_commands(
            "configure_mid", command_input_factory
        )
        csp_input_json = prepare_json_args_for_commands(
            "csp_configure_mid", command_input_factory
        )
        csp_mock = mock_factory.get_or_create_mock_device(
            MockDeviceType.CSP_DEVICE
        )

        event_recorder.subscribe_event(subarray_node.subarray_node, "obsState")
        subarray_node.move_to_on()
        subarray_node.force_change_of_obs_state("IDLE")

        # CSP should go to configuring in no more than 0.1 sec
        obs_state_duration_params = '[["CONFIGURING",0.1]]'
        csp_mock.AddTransition(obs_state_duration_params)

        subarray_node.execute_transition("Configure", argin=input_json)

        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node, "obsState", ObsState.CONFIGURING
        )

        with pytest.raises(AssertionError):
            assert event_recorder.has_change_event_occurred(
                subarray_node.subarray_node, "obsState", ObsState.READY
            )
        # Add assert for commandCallInfo data
        assert device_is_with_correct_command_recorder_data(
            csp_mock, "Configure", csp_input_json
        )
