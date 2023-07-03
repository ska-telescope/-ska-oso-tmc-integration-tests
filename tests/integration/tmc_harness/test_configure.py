import pytest

from tests.resources.test_harness.helpers import check_subarray_obs_state


class TestSubarrayNodeObsStateTransitions(object):
    @pytest.mark.parametrize(
        "source_obs_state, trigger, args_to_the_command, destination_obs_state",
        [
            ("IDLE", "Configure", "configure_mid", "READY"),
            ("READY", "End", None, "IDLE"),
        ],
    )
    @pytest.mark.SKA_mid
    def test_subarray_obs_transitions_valid_data(
        self,
        subarray_node,
        command_input_factory,
        source_obs_state,
        trigger,
        args_to_the_command,
        destination_obs_state,
    ):
        # TODO: WIP
        # sdp_mock = mock_factory.create_sdp_mock("configure", duration = 20)

        if args_to_the_command is not None:
            input_json = command_input_factory.create_subarray_configuration(
                args_to_the_command
            )
        else:
            input_json = None

        if subarray_node.state != subarray_node.ON_STATE:
            subarray_node.move_to_on()

        if subarray_node.obs_state != source_obs_state:
            subarray_node.force_change_obs_state(source_obs_state)

        subarray_node.execute_transition(trigger, argin=input_json)

        assert check_subarray_obs_state(
            obs_state=destination_obs_state, timeout=500
        )

        # assert_that(subarray_node.obs_state).is_equal_to(
        #     subarray_node.READY_OBS_STATE
        # )
