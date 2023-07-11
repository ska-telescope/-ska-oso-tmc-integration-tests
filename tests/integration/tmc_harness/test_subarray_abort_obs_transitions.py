import pytest

from tests.resources.test_harness.helpers import (
    check_subarray_obs_state,
    get_device_mocks,
)


class TestSubarrayNodeAbortCommandObsStateTransitions(object):
    @pytest.mark.parametrize(
        "source_obs_state",
        [
            "IDLE",
            "SCANNING",
            "READY",
            "RESOURCING",
            "CONFIGURING",
        ],
    )
    @pytest.mark.SKA_mid
    def test_subarray_obs_transitions_valid_data(
        self,
        subarray_node,
        mock_factory,
        source_obs_state,
    ):
        """
        Test to verify transitions that are triggered by Abort
        command and followed by a completion transition
        that start with a transient state.
        assuming that external subsystems work fine.
        Glossary:
        - "subarray_node": fixture for a TMC SubarrayNode under test
        - "mock_factory": fixture for MockFactory class
        - "source_obs_state": a TMC SubarrayNode initial allowed obsState,
           required to invoke Abort command
        """
        csp_mock, _, _, sdp_mock = get_device_mocks(mock_factory)

        obs_state_transition_duration_sec = 30

        delay_command_params_str = '{"Abort": %s}' % (
            obs_state_transition_duration_sec
        )

        sdp_mock.setDelay(delay_command_params_str)
        csp_mock.setDelay(delay_command_params_str)

        subarray_node.move_to_on()

        subarray_node.force_change_of_obs_state(source_obs_state)

        subarray_node.execute_transition("Abort", argin=None)

        # As we set Obs State transition duration to 30 so wait timeout here
        # provided as 32 sec. It validate after 32 sec excepted
        # obs state change
        expected_timeout_sec = obs_state_transition_duration_sec + 2

        assert check_subarray_obs_state(
            obs_state=subarray_node.ABORTED_OBS_STATE,
            timeout=expected_timeout_sec,
        )
