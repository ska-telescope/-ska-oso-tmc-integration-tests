from typing import Any

import pytest
from ska_tango_base.control_model import ObsState

from tests.resources.test_harness.helpers import (
    check_subarray_obs_state,
    get_device_mocks,
)


class TestSubarrayNodeObsStateTransitions(object):
    @pytest.mark.parametrize(
        "source_obs_state, trigger, args_for_command, destination_obs_state",
        [
            ("READY", "End", None, "IDLE"),
            ("RESOURCING", None, None, "IDLE"),
            ("CONFIGURING", None, None, "READY"),
            ("SCANNING", None, None, "READY"),
            ("ABORTED", "Restart", None, "EMPTY"),
        ],
    )
    @pytest.mark.SKA_mid
    def test_subarray_obs_transitions_valid_data(
        self,
        subarray_node,
        command_input_factory,
        mock_factory,
        source_obs_state,
        trigger,
        args_for_command,
        destination_obs_state,
    ):
        """
        Test to verify transitions that are triggered by a command
        and followed by a completion transition, or
        individual transitions that start with a transient state.
        assuming that external subsystems work fine.
        Glossary:
        - "completion transition" : a transition that exits a state and
           is not triggered by a command
        - "transient state": a state that has at least one completion
           transition
        - "subarray_node": fixture for a TMC SubarrayNode under test
        - "command_input_factory": fixture for JsonFactory class
        - "mock_factory": fixture for MockFactory class
        - "source_obs_state": a TMC SubarrayNode initial allowed obsState,
           required for triggered a command
        - "trigger": a command name
        - "args_for_command": input arguments required for triggered
           command
        - "destination_obs_state": a TMC SubarrayNode final obsState,
           representing a successful completion of triggered command
        """

        input_json = self.prepare_json_args_for_commands(
            args_for_command, command_input_factory
        )
        csp_mock, dish_mock_1, dish_mock_2, sdp_mock = get_device_mocks(
            mock_factory
        )

        obs_state_transition_duration_sec = 30

        delay_command_params_str = '{"%s": %s}' % (
            trigger,
            obs_state_transition_duration_sec,
        )

        sdp_mock.setDelay(delay_command_params_str)
        csp_mock.setDelay(delay_command_params_str)
        dish_mock_1.setDelay(delay_command_params_str)
        dish_mock_2.setDelay(delay_command_params_str)

        subarray_node.move_to_on()

        subarray_node.force_change_of_obs_state(source_obs_state)

        subarray_node.execute_transition(trigger, argin=input_json)

        # As we set Obs State transition duration to 30 so wait timeout here
        # provided as 32 sec. It validate after 32 sec excepted
        # obs state change
        expected_timeout_sec = obs_state_transition_duration_sec + 2

        assert check_subarray_obs_state(
            obs_state=destination_obs_state, timeout=expected_timeout_sec
        )

    @pytest.mark.hope
    @pytest.mark.SKA_mid
    @pytest.mark.parametrize(
        "source_obs_state, trigger, args_for_command,\
            intermediate_obs_state, destination_obs_state,\
            args_for_csp, args_for_sdp",
        [
            (
                "IDLE",
                "Configure",
                "configure_mid",
                ObsState.CONFIGURING,
                ObsState.READY,
                "csp_configure_mid",
                "sdp_configure_mid",
            ),
            (
                "EMPTY",
                "AssignResources",
                "assign_resources_mid",
                ObsState.RESOURCING,
                ObsState.IDLE,
                "csp_assign_resources_mid",
                "sdp_assign_resources_mid",
            ),
            (
                "READY",
                "Scan",
                "scan_mid",
                ObsState.SCANNING,
                ObsState.READY,
                "csp_scan_mid",
                "sdp_scan_mid",
            ),
        ],
    )
    @pytest.mark.SKA_mid
    def test_subarray_pair_transition(
        self,
        subarray_node,
        command_input_factory,
        mock_factory,
        event_recorder,
        source_obs_state,
        trigger,
        args_for_command,
        intermediate_obs_state,
        destination_obs_state,
        args_for_csp,
        args_for_sdp,
    ):
        """This test case validate pair of transition triggered by command"""
        input_json = self.prepare_json_args_for_commands(
            args_for_command, command_input_factory
        )
        csp_input_json = self.prepare_json_args_for_commands(
            args_for_csp, command_input_factory
        )
        sdp_input_json = self.prepare_json_args_for_commands(
            args_for_sdp, command_input_factory
        )
        obs_state_transition_duration_sec = 30
        delay_command_params_str = '{"%s": %s}' % (
            trigger,
            obs_state_transition_duration_sec,
        )

        csp_mock, sdp_mock, dish_mock_1, dish_mock_2 = get_device_mocks(
            mock_factory
        )
        sdp_mock.setDelay(delay_command_params_str)
        csp_mock.setDelay(delay_command_params_str)
        dish_mock_1.setDelay(delay_command_params_str)
        dish_mock_2.setDelay(delay_command_params_str)

        event_recorder.subscribe_event(subarray_node.subarray_node, "obsState")
        event_recorder.subscribe_event(sdp_mock, "commandCallInfo")
        event_recorder.subscribe_event(csp_mock, "commandCallInfo")

        subarray_node.move_to_on()
        subarray_node.force_change_of_obs_state(source_obs_state)

        subarray_node.execute_transition(trigger, argin=input_json)

        # Validate subarray node goes into CONFIGURING obs state first
        # This assertion fail if obsState attribute value is not
        # changed to CONFIGURING within 7 events for obsState of subarray node
        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node, "obsState", intermediate_obs_state
        )
        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node, "obsState", destination_obs_state
        )
        assert self.device_is_with_correct_command_data(
            csp_mock, trigger, csp_input_json
        )
        assert self.device_is_with_correct_command_data(
            sdp_mock, trigger, sdp_input_json
        )
        assert self.single_command_entry_in_command_data(csp_mock)
        assert self.single_command_entry_in_command_data(sdp_mock)

    # following is a helper method
    def prepare_json_args_for_commands(
        self, args_for_command, command_input_factory
    ):
        if args_for_command is not None:
            input_json = command_input_factory.create_subarray_configuration(
                args_for_command
            )
        else:
            input_json = None
        return input_json

    def get_command_call_info(self, device: Any):
        """
        device: Tango Device Proxy Object

        """
        command_call_info = device.read_attribute("commandCallInfo").value
        input_str = "".join(command_call_info[0][1].split())
        received_command_call_data = (
            command_call_info[0][0],
            sorted(input_str),
        )
        return received_command_call_data

    def device_is_with_correct_command_data(
        self, device: Any, expected_command_name: str, expected_inp_str: str
    ):
        """_summary_"""

        received_command_call_data = self.get_command_call_info(device)

        expected_input_str = "".join(expected_inp_str.split())

        return received_command_call_data == (
            expected_command_name,
            sorted(expected_input_str),
        )

    def single_command_entry_in_command_data(self, device: Any):
        command_call_info = device.read_attribute("commandCallInfo").value
        return len(command_call_info) == 1
