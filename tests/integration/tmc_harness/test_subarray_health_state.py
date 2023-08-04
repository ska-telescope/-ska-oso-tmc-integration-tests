import pytest
from ska_tango_base.control_model import HealthState, ObsState

from tests.resources.test_harness.helpers import (
    get_device_simulators,
    prepare_json_args_for_commands,
)


class TestSubarrayHealthState(object):
    """This class implement test cases to verify HealthState
    of Subarray Node.
    This tests implement rows of following excel sheet
    https://docs.google.com/spreadsheets/d/1XbNb8We7fK-EhmOcw3S-h0V_Pu-WAfPTkEd13MSmIns/edit#gid=747888622
    """

    @pytest.mark.invalid
    @pytest.mark.SKA_mid
    def test_health_state_ok(
        self, subarray_node, simulator_factory, event_recorder
    ):
        # Row 1
        (
            csp_sa_sim,
            sdp_sa_sim,
            dish_master_1,
            dish_master_2,
        ) = get_device_simulators(simulator_factory)

        csp_sa_sim.SetDirectHealthState(HealthState.OK)
        sdp_sa_sim.SetDirectHealthState(HealthState.OK)
        dish_master_1.SetDirectHealthState(HealthState.OK)
        dish_master_2.SetDirectHealthState(HealthState.OK)

        event_recorder.subscribe_event(
            subarray_node.subarray_node, "healthState"
        )
        # Subarray node react automatically
        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node,
            "healthState",
            HealthState.OK,
        ), "Expected Subarray Node HealthState to be OK"

    @pytest.mark.invalid
    @pytest.mark.SKA_mid
    def test_health_state_failed_when_csp_failed(
        self, subarray_node, simulator_factory, event_recorder
    ):
        # Row 2
        (
            csp_sa_sim,
            sdp_sa_sim,
            dish_master_1,
            dish_master_2,
        ) = get_device_simulators(simulator_factory)

        csp_sa_sim.SetDirectHealthState(HealthState.FAILED)
        sdp_sa_sim.SetDirectHealthState(HealthState.OK)
        dish_master_1.SetDirectHealthState(HealthState.OK)
        dish_master_2.SetDirectHealthState(HealthState.OK)

        event_recorder.subscribe_event(
            subarray_node.subarray_node, "healthState"
        )

        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node,
            "healthState",
            HealthState.FAILED,
        ), "Expected Subarray Node HealthState to be FAILED"

    @pytest.mark.invalid
    @pytest.mark.SKA_mid
    def test_health_state_degraded_when_csp_degraded(
        self, subarray_node, simulator_factory, event_recorder
    ):
        # Row 3
        (
            csp_sa_sim,
            sdp_sa_sim,
            dish_master_1,
            dish_master_2,
        ) = get_device_simulators(simulator_factory)

        csp_sa_sim.SetDirectHealthState(HealthState.DEGRADED)
        sdp_sa_sim.SetDirectHealthState(HealthState.OK)
        dish_master_1.SetDirectHealthState(HealthState.OK)
        dish_master_2.SetDirectHealthState(HealthState.OK)

        event_recorder.subscribe_event(
            subarray_node.subarray_node, "healthState"
        )

        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node,
            "healthState",
            HealthState.DEGRADED,
        ), "Expected Subarray Node HealthState to be DEGRADED"

    @pytest.mark.negative
    @pytest.mark.SKA_mid
    def test_health_state_failed_when_sdp_failed(
        self, subarray_node, simulator_factory, event_recorder
    ):
        # Row 5
        (
            csp_sa_sim,
            sdp_sa_sim,
            dish_master_1,
            dish_master_2,
        ) = get_device_simulators(simulator_factory)

        csp_sa_sim.SetDirectHealthState(HealthState.OK)
        sdp_sa_sim.SetDirectHealthState(HealthState.FAILED)
        dish_master_1.SetDirectHealthState(HealthState.OK)
        dish_master_2.SetDirectHealthState(HealthState.OK)

        event_recorder.subscribe_event(
            subarray_node.subarray_node, "healthState"
        )

        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node,
            "healthState",
            HealthState.OK,
        ), "Expected Subarray Node HealthState to be FAILED"

    @pytest.mark.invalid
    @pytest.mark.SKA_mid
    def test_health_state_failed_when_dish_failed(
        self,
        subarray_node,
        simulator_factory,
        event_recorder,
        command_input_factory,
    ):
        # Row 9
        (
            csp_sa_sim,
            sdp_sa_sim,
            dish_master_1,
            dish_master_2,
        ) = get_device_simulators(simulator_factory)

        self._assign_dishes_to_subarray(
            subarray_node, command_input_factory, event_recorder
        )

        csp_sa_sim.SetDirectHealthState(HealthState.OK)
        sdp_sa_sim.SetDirectHealthState(HealthState.OK)
        dish_master_1.SetDirectHealthState(HealthState.FAILED)
        dish_master_2.SetDirectHealthState(HealthState.FAILED)

        event_recorder.subscribe_event(
            subarray_node.subarray_node, "healthState"
        )

        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node,
            "healthState",
            HealthState.FAILED,
        ), "Expected Subarray Node HealthState to be FAILED"

    @pytest.mark.invalid
    @pytest.mark.SKA_mid
    def test_health_state_one_dish_failed(
        self,
        subarray_node,
        simulator_factory,
        event_recorder,
        command_input_factory,
    ):
        # Row 8
        (
            csp_sa_sim,
            sdp_sa_sim,
            dish_master_1,
            dish_master_2,
        ) = get_device_simulators(simulator_factory)

        self._assign_dishes_to_subarray(
            subarray_node, command_input_factory, event_recorder
        )

        csp_sa_sim.SetDirectHealthState(HealthState.OK)
        sdp_sa_sim.SetDirectHealthState(HealthState.OK)
        dish_master_1.SetDirectHealthState(HealthState.FAILED)
        dish_master_2.SetDirectHealthState(HealthState.OK)

        event_recorder.subscribe_event(
            subarray_node.subarray_node, "healthState"
        )

        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node,
            "healthState",
            HealthState.DEGRADED,
        ), "Expected Subarray Node HealthState to be DEGRADED"

    def _assign_dishes_to_subarray(
        self, subarray_node, command_input_factory, event_recorder
    ):
        subarray_node.move_to_on()
        subarray_node.force_change_of_obs_state("EMPTY")
        input_json = prepare_json_args_for_commands(
            "assign_resources_mid", command_input_factory
        )

        event_recorder.subscribe_event(subarray_node.subarray_node, "obsState")

        subarray_node.execute_transition("AssignResources", argin=input_json)
        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node, "obsState", ObsState.IDLE
        ), "Waiting for subarray node to complete"
