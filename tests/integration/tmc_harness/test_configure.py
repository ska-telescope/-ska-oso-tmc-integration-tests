import pytest
from assertpy import assert_that


class TestSubarrayNodeObsStateTransitions(object):
    @pytest.mark.hope
    @pytest.mark.SKA_mid
    def test_idle_to_ready_valid_data(
        self, subarray_node, command_input_factory
    ):
        # TODO: WIP
        # sdp_mock = mock_factory.create_sdp_mock("configure", duration = 20)

        configure_json = command_input_factory.create_subarray_configuration(
            "configure_mid"
        )
        if subarray_node.state != subarray_node.ON_STATE:
            subarray_node.move_to_on()

        if subarray_node.obs_state != subarray_node.IDLE_OBS_STATE:
            subarray_node.force_change_obs_state(subarray_node.IDLE_OBS_STATE)

        subarray_node.configure_subarray(configure_json)

        assert_that(subarray_node.obs_state).is_equal_to(
            subarray_node.READY_OBS_STATE
        )
