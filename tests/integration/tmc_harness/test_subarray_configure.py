"""This module implements test case for Configure command."""
import pytest
from ska_control_model import ObsState

from tests.resources.test_harness.helpers import (
    check_subarray_obs_state,
    prepare_json_args_for_commands,
)


class TestMidSubarrayNodeConfigure:
    """This class tests the Configure command on Subarray Node"""

    @pytest.mark.only_configure
    def test_subarray_configure(
        self, subarray_node, event_recorder, command_input_factory
    ):
        """This tests configure command flow on Subarray Node."""
        configure_command_input = prepare_json_args_for_commands(
            "configure_mid", command_input_factory
        )
        scan_command_input = prepare_json_args_for_commands(
            "scan_mid", command_input_factory
        )
        partial_configure_1 = prepare_json_args_for_commands(
            "partial_configure_1", command_input_factory
        )
        partial_configure_2 = prepare_json_args_for_commands(
            "partial_configure_2", command_input_factory
        )
        partial_configure_3 = prepare_json_args_for_commands(
            "partial_configure_3", command_input_factory
        )
        partial_configure_4 = prepare_json_args_for_commands(
            "partial_configure_4", command_input_factory
        )
        event_recorder.subscribe_event(subarray_node.subarray_node, "obsState")
        event_recorder.subscribe_event(
            subarray_node.csp_subarray_leaf_node, "cspSubarrayObsState"
        )
        event_recorder.subscribe_event(
            subarray_node.sdp_subarray_leaf_node, "sdpSubarrayObsState"
        )

        subarray_node.move_to_on()

        subarray_node.force_change_of_obs_state("IDLE")
        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node,
            "obsState",
            ObsState["IDLE"],
            lookahead=15,
        )
        assert event_recorder.has_change_event_occurred(
            subarray_node.csp_subarray_leaf_node,
            "cspSubarrayObsState",
            ObsState["IDLE"],
            lookahead=15,
        )
        assert event_recorder.has_change_event_occurred(
            subarray_node.sdp_subarray_leaf_node,
            "sdpSubarrayObsState",
            ObsState["IDLE"],
            lookahead=15,
        )

        subarray_node.execute_transition("Configure", configure_command_input)

        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node,
            "obsState",
            ObsState.CONFIGURING,
            lookahead=15,
        )

        assert event_recorder.has_change_event_occurred(
            subarray_node.sdp_subarray_leaf_node,
            "sdpSubarrayObsState",
            ObsState.READY,
            lookahead=15,
        )
        assert event_recorder.has_change_event_occurred(
            subarray_node.csp_subarray_leaf_node,
            "cspSubarrayObsState",
            ObsState.READY,
            lookahead=15,
        )
        assert check_subarray_obs_state(obs_state="READY")

        # Scan
        subarray_node.execute_transition("Scan", scan_command_input)

        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node,
            "obsState",
            ObsState.SCANNING,
            lookahead=15,
        )

        assert check_subarray_obs_state(obs_state="READY")

        # Partial configure 1
        subarray_node.execute_transition("Configure", partial_configure_1)

        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node,
            "obsState",
            ObsState.CONFIGURING,
            lookahead=15,
        )

        assert check_subarray_obs_state(obs_state="READY")

        subarray_node.execute_transition("Scan", scan_command_input)

        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node,
            "obsState",
            ObsState.SCANNING,
            lookahead=15,
        )

        assert check_subarray_obs_state(obs_state="READY")

        # Partial configure 2
        subarray_node.execute_transition("Configure", partial_configure_2)

        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node,
            "obsState",
            ObsState.CONFIGURING,
            lookahead=15,
        )

        assert check_subarray_obs_state(obs_state="READY")

        subarray_node.execute_transition("Scan", scan_command_input)

        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node,
            "obsState",
            ObsState.SCANNING,
            lookahead=15,
        )

        assert check_subarray_obs_state(obs_state="READY")

        # Partial configure 3
        subarray_node.execute_transition("Configure", partial_configure_3)

        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node,
            "obsState",
            ObsState.CONFIGURING,
            lookahead=15,
        )

        assert check_subarray_obs_state(obs_state="READY")

        subarray_node.execute_transition("Scan", scan_command_input)

        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node,
            "obsState",
            ObsState.SCANNING,
            lookahead=15,
        )

        assert check_subarray_obs_state(obs_state="READY")

        # Partial configure 4
        subarray_node.execute_transition("Configure", partial_configure_4)

        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node,
            "obsState",
            ObsState.CONFIGURING,
            lookahead=15,
        )

        assert check_subarray_obs_state(obs_state="READY")

        subarray_node.execute_transition("Scan", scan_command_input)

        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node,
            "obsState",
            ObsState.SCANNING,
            lookahead=15,
        )

        assert check_subarray_obs_state(obs_state="READY")
