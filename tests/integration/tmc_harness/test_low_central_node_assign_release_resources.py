import pytest
from ska_control_model import ObsState

from tests.resources.test_harness.helpers import (
    prepare_json_args_for_centralnode_commands,
)
from tests.resources.test_harness.utils.enums import SimulatorDeviceType
from tango import DevState

class TestLowCentralNodeAssignResources(object):
    # @pytest.mark.skip(
    #     reason="AssignResources and ReleaseResources"
    #     " functionalities are not yet"
    #     " implemented on mccs master leaf node."
    # )
    @pytest.mark.SKA_low131
    def test_low_centralnode_assign_resources(
        self,
        central_node_low,
        event_recorder,
        simulator_factory,
        command_input_factory,
    ):
        """
        Test to verify transitions that are triggered by AssignResources
        command and followed by a completion transition
        assuming that external subsystems work fine.
        Glossary:
        - "central_node_low": fixture for a TMC CentralNode Low under test
        which provides simulated master devices
        - "event_recorder": fixture for a MockTangoEventCallbackGroup
        for validating the subscribing and receiving events.
        - "simulator_factory": fixtur for creating simulator devices for
        low Telescope respectively.
        - "command_input_factory": fixture for JsonFactory class,
        which provides json files for CentralNode
        """
        assign_input_json = prepare_json_args_for_centralnode_commands(
            "assign_resources_low", command_input_factory
        )
        csp_master_sim = simulator_factory.get_or_create_simulator_device(
            SimulatorDeviceType.LOW_CSP_DEVICE
        )
        sdp_master_sim = simulator_factory.get_or_create_simulator_device(
            SimulatorDeviceType.LOW_SDP_DEVICE
        )
        mccs_master_sim = simulator_factory.get_or_create_simulator_device(
            SimulatorDeviceType.MCCS_MASTER_DEVICE
        )
        event_recorder.subscribe_event(csp_master_sim, "State")
        event_recorder.subscribe_event(sdp_master_sim, "State")
        event_recorder.subscribe_event(mccs_master_sim, "State")
        event_recorder.subscribe_event(
            central_node_low.central_node, "telescopeState"
        )
        event_recorder.subscribe_event(csp_master_sim, "obsState")
        event_recorder.subscribe_event(sdp_master_sim, "obsState")
        #event_recorder.subscribe_event(mccs_master_sim, "obsState")
        event_recorder.subscribe_event(
            central_node_low.subarray_node, "obsState"
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
        assert event_recorder.has_change_event_occurred(
            mccs_master_sim,
            "State",
            DevState.ON,
        )
        assert event_recorder.has_change_event_occurred(
            central_node_low.central_node,
            "telescopeState",
            DevState.ON,
        )

        central_node_low.perform_action("AssignResources", assign_input_json)
        assert event_recorder.has_change_event_occurred(
            sdp_master_sim,
            "obsState",
            ObsState.IDLE,
        )
        assert event_recorder.has_change_event_occurred(
            csp_master_sim,
            "obsState",
            ObsState.IDLE,
        )
        # assert event_recorder.has_change_event_occurred(
        #     mccs_master_sim,
        #     "State",
        #     ObsState.IDLE,
        # )
        assert event_recorder.has_change_event_occurred(
            central_node_low.subarray_node,
            "obsState",
            ObsState.IDLE,
        )
