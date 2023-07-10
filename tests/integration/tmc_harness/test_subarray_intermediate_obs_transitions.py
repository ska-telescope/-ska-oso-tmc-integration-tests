import pytest
from assertpy import assert_that


class TestSubarrayNodeIntermediateObsStateTransitions(object):
    @pytest.mark.parametrize(
        "source_obs_state, trigger, args_for_command, intermediate_obs_state",
        [
            ("IDLE", "AssignResources", "assign_resources_mid", "RESOURCING"),
            ("IDLE", "Configure", "configure_mid", "CONFIGURING"),
            ("READY", "Scan", "scan_mid", "SCANNING"),
        ],
    )
    @pytest.mark.SKA_mid
    def test_subarray_intermediate_obs_transitions_valid_data(
        self,
        subarray_node,
        command_input_factory,
        source_obs_state,
        trigger,
        args_for_command,
        intermediate_obs_state,
    ):

        if args_for_command is not None:
            input_json = command_input_factory.create_subarray_configuration(
                args_for_command
            )
        else:
            input_json = None

        subarray_node.move_to_on()

        subarray_node.force_change_of_obs_state(source_obs_state)

        subarray_node.execute_transition(trigger, argin=input_json)

        assert_that(subarray_node.obs_state).is_equal_to(
            intermediate_obs_state
        )
