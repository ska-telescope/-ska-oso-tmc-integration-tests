import pytest

from tests.resources.test_harness.helpers import check_subarray_obs_state


class TestSubarrayNodeObsStateTransitions(object):
    @pytest.mark.skip(reason="Scenario is covered in another file")
    @pytest.mark.SKA_mid
    def test_ready_to_idle_valid_data(self, subarray_node):
        if subarray_node.state != subarray_node.ON_STATE:
            subarray_node.move_to_on()

        if subarray_node.obs_state != subarray_node.READY_OBS_STATE:
            subarray_node.force_change_obs_state(subarray_node.READY_OBS_STATE)

        subarray_node.execute_transition("End", argin=None)

        # assert_that(subarray_node.obs_state).is_equal_to(
        #     subarray_node.IDLE_OBS_STATE
        # )
        assert check_subarray_obs_state(
            obs_state=subarray_node.IDLE_OBS_STATE, timeout=500
        )
