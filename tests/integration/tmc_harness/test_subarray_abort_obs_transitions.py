import pytest

from tests.resources.test_harness.helpers import check_subarray_obs_state
from tests.resources.test_harness.utils.enums import MockDeviceType


class TestSubarrayNodeAbortCommandObsStateTransitions(object):
    @pytest.mark.abort
    @pytest.mark.parametrize(
        "source_obs_state",
        [
            "SCANNING",
            "READY",
        ],
    )
    @pytest.mark.SKA_mid
    def test_subarray_obs_transitions_valid_data(
        self,
        subarray_node,
        mock_factory,
        source_obs_state,
    ):

        sdp_mock = mock_factory.get_or_create_mock_device(
            MockDeviceType.SDP_DEVICE
        )

        sdp_mock.setDelay('{"Abort": 30}')

        csp_mock = mock_factory.get_or_create_mock_device(
            MockDeviceType.CSP_DEVICE
        )

        csp_mock.setDelay('{"Abort": 30}')

        # csp_mock.SetDefective(True)

        # sdp_mock.SetDefective(True)

        subarray_node.move_to_on()

        subarray_node.force_change_of_obs_state(source_obs_state)

        # Setting CSP back to normal
        # csp_mock.SetDefective(False)
        # # Setting SDP back to normal
        # sdp_mock.SetDefective(False)

        subarray_node.execute_transition("Abort", argin=None)

        assert check_subarray_obs_state(
            obs_state=subarray_node.ABORTED_OBS_STATE, timeout=32
        )
