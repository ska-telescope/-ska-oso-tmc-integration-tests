import pytest
from ska_control_model import ObsState
from tango import DevState

from tests.resources.test_harness.helpers import (
    get_device_simulators,
    get_master_device_simulators,
    prepare_json_args_for_centralnode_commands,
)
from tests.resources.test_harness.utils.enums import DishMode


class TestMidCentralNodeStateTransition(object):
    @pytest.mark.assign
    @pytest.mark.SKA_mid
    def test_mid_centralnode_state_transitions(
        self,
        central_node_mid,
        subarray_node,
        event_recorder,
        simulator_factory,
        command_input_factory,
    ):
        """
        Test to verify transitions that are triggered by On
        command and followed by a completion transition
        assuming that external subsystems work fine.
        Glossary:
        - "central_node_mid": fixture for a TMC CentralNode Mid under test
        which provides simulated master devices
        - "event_recorder": fixture for a MockTangoEventCallbackGroup
        for validating the subscribing and receiving events.
        - "simulator_factory": fixtur for creating simulator devices for
        mid Telescope respectively.
        """
        assign_input_json = prepare_json_args_for_centralnode_commands(
            "assign_resources_mid", command_input_factory
        )
        release_input_json = prepare_json_args_for_centralnode_commands(
            "release_resources_mid", command_input_factory
        )
        (
            csp_master_sim,
            sdp_master_sim,
            dish_master_sim1,
            dish_master_sim2,
        ) = get_master_device_simulators(simulator_factory)
        csp_sim, sdp_sim, _, _ = get_device_simulators(simulator_factory)

        event_recorder.subscribe_event(csp_master_sim, "State")
        event_recorder.subscribe_event(sdp_master_sim, "State")
        event_recorder.subscribe_event(dish_master_sim1, "DishMode")
        event_recorder.subscribe_event(dish_master_sim2, "DishMode")
        event_recorder.subscribe_event(csp_sim, "obsState")
        event_recorder.subscribe_event(sdp_sim, "obsState")
        event_recorder.subscribe_event(subarray_node.subarray_node, "obsState")

        central_node_mid.move_to_on()
        assert event_recorder.has_change_event_occurred(
            csp_master_sim,
            "State",
            DevState.ON,
        )
        assert event_recorder.has_change_event_occurred(
            sdp_master_sim,
            "State",
            DevState.ON,
        )

        central_node_mid.invoke_assign_resources(assign_input_json)
        assert event_recorder.has_change_event_occurred(
            sdp_sim,
            "obsState",
            ObsState.IDLE,
        )
        assert event_recorder.has_change_event_occurred(
            csp_sim,
            "obsState",
            ObsState.IDLE,
        )
        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node,
            "obsState",
            ObsState.IDLE,
        )

        central_node_mid.invoke_release_resources(release_input_json)
        assert event_recorder.has_change_event_occurred(
            sdp_sim,
            "obsState",
            ObsState.EMPTY,
        )
        assert event_recorder.has_change_event_occurred(
            csp_sim,
            "obsState",
            ObsState.EMPTY,
        )
        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node,
            "obsState",
            ObsState.EMPTY,
        )

        # As there is inconsistancy between the states of Dish Master and other
        # subsystem that's why Dishmode is considered for DishMaster
        # transitions. Here is the link for reference.
        # https://confluence.skatelescope.org/display/SE/Subarray+obsMode+and+
        # Dish+states+and+modes
        assert event_recorder.has_change_event_occurred(
            dish_master_sim1,
            "DishMode",
            DishMode.STANDBY_FP,
        )
        assert event_recorder.has_change_event_occurred(
            dish_master_sim2,
            "DishMode",
            DishMode.STANDBY_FP,
        )
