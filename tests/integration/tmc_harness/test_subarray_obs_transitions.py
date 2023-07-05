import pytest

from tests.resources.test_harness.helpers import check_subarray_obs_state
from tests.resources.test_harness.utils.enums import MockDeviceType


class TestSubarrayNodeObsStateTransitions(object):
    @pytest.mark.configure
    @pytest.mark.parametrize(
        "source_obs_state, trigger, args_for_command, destination_obs_state",
        [
            ("IDLE", "Configure", "configure_mid", "READY"),
            ("READY", "End", None, "IDLE"),
            ("EMPTY", "AssignResources", "assign_resources_mid", "IDLE"),
            ("CONFIGURING", None, None, "READY"),
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

        sdp_mock = mock_factory.get_or_create_mock_device(
            MockDeviceType.SDP_DEVICE
        )

        sdp_mock.setDelay('{"Configure": 30}')

        csp_mock = mock_factory.get_or_create_mock_device(
            MockDeviceType.CSP_DEVICE
        )

        csp_mock.setDelay('{"Configure": 30}')

        if args_for_command is not None:
            input_json = command_input_factory.create_subarray_configuration(
                args_for_command
            )
        else:
            input_json = None

        if subarray_node.state != subarray_node.ON_STATE:
            subarray_node.move_to_on()

        if subarray_node.obs_state != source_obs_state:
            subarray_node.force_change_of_obs_state(source_obs_state)

        subarray_node.execute_transition(trigger, argin=input_json)

        assert check_subarray_obs_state(
            obs_state=destination_obs_state, timeout=320
        )
