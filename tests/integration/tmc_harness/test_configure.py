import pytest

from tests.resources.test_harness.helpers import check_subarray_obs_state


class TestSubarrayNodeObsStateTransitions(object):
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

        subarray_node.execute_transition("Configure", argin=configure_json)

        assert check_subarray_obs_state(
            obs_state=subarray_node.READY_OBS_STATE, timeout=500
        )

        # assert_that(subarray_node.obs_state).is_equal_to(
        #     subarray_node.READY_OBS_STATE
        # )
