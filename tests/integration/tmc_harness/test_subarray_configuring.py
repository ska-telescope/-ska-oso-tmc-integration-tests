import pytest
from assertpy import assert_that

from tests.resources.test_harness.utils.enums import MockDeviceType


class TestSubarrayNodeObsStateTransitions(object):
    @pytest.mark.parametrize(
        "source_obs_state, trigger, args_for_command, intermediate_obs_state",
        [
            ("IDLE", "Configure", "configure_mid", "CONFIGURING"),
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
        intermediate_obs_state,
    ):

        mock_factory.get_or_create_mock_device(
            MockDeviceType.SDP_DEVICE, obs_state_transition_duration=30
        )

        mock_factory.get_or_create_mock_device(
            MockDeviceType.CSP_DEVICE, obs_state_transition_duration=30
        )

        if args_for_command is not None:
            input_json = command_input_factory.create_subarray_configuration(
                args_for_command
            )
        else:
            input_json = None

        if subarray_node.state != subarray_node.ON_STATE:
            subarray_node.move_to_on()

        if subarray_node.obs_state != source_obs_state:
            subarray_node.force_change_obs_state(source_obs_state)

        subarray_node.execute_transition(trigger, argin=input_json)

        assert_that(subarray_node.obs_state).is_equal_to(
            intermediate_obs_state
        )
