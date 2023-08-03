import pytest
from ska_tango_base.control_model import HealthState, ObsState

from tests.resources.test_harness.helpers import (
    get_device_simulators,
    prepare_json_args_for_commands,
)


class TestSubarrayHealthState(object):
    """This class implement test cases to verify HealthState
    of Subarray Node"""

    @pytest.mark.invalid
    @pytest.mark.SKA_mid
    def test_health_state_ok(
        self, subarray_node, simulator_factory, event_recorder
    ):
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

        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node,
            "healthState",
            HealthState.OK,
        )

    @pytest.mark.invalid
    @pytest.mark.SKA_mid
    def test_health_state_failed(
        self, subarray_node, simulator_factory, event_recorder
    ):
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
        )

    @pytest.mark.invalid
    @pytest.mark.SKA_mid
    def test_health_state_degraded(
        self, subarray_node, simulator_factory, event_recorder
    ):
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
        )

    @pytest.mark.invalid
    @pytest.mark.SKA_mid
    def test_health_state_sdp_failed(
        self, subarray_node, simulator_factory, event_recorder
    ):
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
            HealthState.FAILED,
        )

    @pytest.mark.invalid
    @pytest.mark.SKA_mid
    def test_health_state_dish_failed(
        self,
        subarray_node,
        simulator_factory,
        event_recorder,
        command_input_factory,
    ):
        (
            csp_sa_sim,
            sdp_sa_sim,
            dish_master_1,
            dish_master_2,
        ) = get_device_simulators(simulator_factory)

        subarray_node.move_to_on()
        subarray_node.force_change_of_obs_state("EMPTY")
        input_json = prepare_json_args_for_commands(
            "assign_resources_mid", command_input_factory
        )

        event_recorder.subscribe_event(subarray_node.subarray_node, "obsState")

        subarray_node.execute_transition("AssignResources", argin=input_json)
        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node, "obsState", ObsState.IDLE
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
        )

    @pytest.mark.invalid
    @pytest.mark.SKA_mid
    def test_health_state_one_dish_failed(
        self,
        subarray_node,
        simulator_factory,
        event_recorder,
        command_input_factory,
    ):
        (
            csp_sa_sim,
            sdp_sa_sim,
            dish_master_1,
            dish_master_2,
        ) = get_device_simulators(simulator_factory)

        subarray_node.move_to_on()
        subarray_node.force_change_of_obs_state("EMPTY")
        input_json = prepare_json_args_for_commands(
            "assign_resources_mid", command_input_factory
        )

        event_recorder.subscribe_event(subarray_node.subarray_node, "obsState")

        subarray_node.execute_transition("AssignResources", argin=input_json)
        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node, "obsState", ObsState.IDLE
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
        )
