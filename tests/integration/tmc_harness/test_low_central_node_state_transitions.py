import pytest
from ska_control_model import ObsState
from tango import DevState

from tests.resources.test_harness.helpers import (
    prepare_json_args_for_centralnode_commands,
)
from tests.resources.test_harness.utils.enums import SimulatorDeviceType


class TestLowCentralNodeStateTransition(object):
    @pytest.mark.SKA_low
    @pytest.mark.assignlow
    def test_low_centralnode_state_transitions(
        self,
        central_node_low,
        event_recorder,
        simulator_factory,
        command_input_factory,
    ):
        """
        Test to verify transitions that are triggered by On
        command and followed by a completion transition
        assuming that external subsystems work fine.
        Glossary:
        - "central_node_low": fixture for a TMC CentralNode Low under test
        which provides simulated master devices
        - "event_recorder": fixture for a MockTangoEventCallbackGroup
        for validating the subscribing and receiving events.
        - "simulator_factory": fixtur for creating simulator devices for
        low Telescope respectively.
        """
        assign_input_json = prepare_json_args_for_centralnode_commands(
            "assign_resources_low", command_input_factory
        )
        release_input_json = prepare_json_args_for_centralnode_commands(
            "release_resources_low", command_input_factory
        )
        csp_master_sim = simulator_factory.get_or_create_simulator_device(
            SimulatorDeviceType.LOW_CSP_MASTER_DEVICE
        )
        sdp_master_sim = simulator_factory.get_or_create_simulator_device(
            SimulatorDeviceType.LOW_SDP_MASTER_DEVICE
        )
        csp_sim = simulator_factory.get_or_create_simulator_device(
            SimulatorDeviceType.LOW_CSP_DEVICE
        )
        sdp_sim = simulator_factory.get_or_create_simulator_device(
            SimulatorDeviceType.LOW_SDP_DEVICE
        )

        event_recorder.subscribe_event(csp_master_sim, "State")
        event_recorder.subscribe_event(sdp_master_sim, "State")
        event_recorder.subscribe_event(csp_sim, "obsState")
        event_recorder.subscribe_event(sdp_sim, "obsState")
        event_recorder.subscribe_event(
            central_node_low.subarray_node_low, "obsState"
        )
        central_node_low.move_to_on()

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

        central_node_low.invoke_assign_resources(assign_input_json)
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
            central_node_low.subarray_node_low,
            "obsState",
            ObsState.IDLE,
        )

        central_node_low.invoke_release_resources(release_input_json)
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
            central_node_low.subarray_node_low,
            "obsState",
            ObsState.EMPTY,
        )
