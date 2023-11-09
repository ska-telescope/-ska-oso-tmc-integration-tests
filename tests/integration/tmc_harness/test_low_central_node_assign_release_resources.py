import json

import pytest
from ska_control_model import ObsState
from ska_tango_base.commands import ResultCode
from tango import DevState

from tests.resources.test_harness.helpers import (
    prepare_json_args_for_centralnode_commands,
    prepare_json_args_for_commands,
)
from tests.resources.test_harness.utils.enums import SimulatorDeviceType


class TestLowCentralNodeAssignResources(object):
    @pytest.mark.SKA_low131  # Marker will be removed.
    @pytest.mark.SKA_low
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
        csp_subarray_sim = simulator_factory.get_or_create_simulator_device(
            SimulatorDeviceType.LOW_CSP_DEVICE
        )
        sdp_subarray_sim = simulator_factory.get_or_create_simulator_device(
            SimulatorDeviceType.LOW_SDP_DEVICE
        )
        mccs_controller_sim = simulator_factory.get_or_create_simulator_device(
            SimulatorDeviceType.MCCS_MASTER_DEVICE
        )

        mccs_subarray_sim = simulator_factory.get_or_create_simulator_device(
            SimulatorDeviceType.MCCS_SUBARRAY_DEVICE
        )

        event_recorder.subscribe_event(csp_subarray_sim, "State")
        event_recorder.subscribe_event(sdp_subarray_sim, "State")
        event_recorder.subscribe_event(mccs_controller_sim, "State")
        event_recorder.subscribe_event(
            central_node_low.central_node, "telescopeState"
        )
        event_recorder.subscribe_event(csp_subarray_sim, "obsState")
        event_recorder.subscribe_event(sdp_subarray_sim, "obsState")
        event_recorder.subscribe_event(mccs_subarray_sim, "obsState")
        event_recorder.subscribe_event(
            central_node_low.subarray_node, "obsState"
        )
        event_recorder.subscribe_event(
            central_node_low.central_node, "longRunningCommandResult"
        )

        event_recorder.subscribe_event(
            central_node_low.subarray_node, "assignedResources"
        )

        # Execute ON Command
        central_node_low.move_to_on()

        assert event_recorder.has_change_event_occurred(
            csp_subarray_sim,
            "State",
            DevState.ON,
        )
        assert event_recorder.has_change_event_occurred(
            sdp_subarray_sim,
            "State",
            DevState.ON,
        )
        assert event_recorder.has_change_event_occurred(
            mccs_controller_sim,
            "State",
            DevState.ON,
        )
        assert event_recorder.has_change_event_occurred(
            central_node_low.central_node,
            "telescopeState",
            DevState.ON,
        )

        # Execute Assign command and perform validations
        result, message = central_node_low.perform_action(
            "AssignResources", assign_input_json
        )

        assigned_resources_json = prepare_json_args_for_commands(
            "AssignedResources_low", command_input_factory
        )

        mccs_subarray_sim.SetDirectassignedResources(assigned_resources_json)

        assert event_recorder.has_change_event_occurred(
            sdp_subarray_sim,
            "obsState",
            ObsState.IDLE,
        )
        assert event_recorder.has_change_event_occurred(
            csp_subarray_sim,
            "obsState",
            ObsState.IDLE,
        )
        assert event_recorder.has_change_event_occurred(
            mccs_subarray_sim,
            "obsState",
            ObsState.IDLE,
        )
        assert event_recorder.has_change_event_occurred(
            central_node_low.subarray_node,
            "obsState",
            ObsState.IDLE,
        )

        assert event_recorder.has_change_event_occurred(
            central_node_low.central_node,
            "longRunningCommandResult",
            (message[0], str(ResultCode.OK.value)),
        )

        # Check if assignedResources attribute is set
        assigned_resources_attribute_value = (
            central_node_low.subarray_node.assignedResources
        )

        assigned_resources = json.loads(assigned_resources_attribute_value[0])
        assert assigned_resources["subarray_beam_ids"] == ["1"]
        assert assigned_resources["channels"] == [32]
        assert assigned_resources["station_ids"] == ["1", "2", "3"]
        assert assigned_resources["apertures"] == [
            "AP001.01",
            "AP001.02",
            "AP002.01",
            "AP002.02",
            "AP003.01",
        ]

        # Execute release command and verify
        release_resource_json = prepare_json_args_for_centralnode_commands(
            "release_resources_low", command_input_factory
        )

        result, message = central_node_low.perform_action(
            "ReleaseResources", release_resource_json
        )

        assert event_recorder.has_change_event_occurred(
            sdp_subarray_sim,
            "obsState",
            ObsState.EMPTY,
        )
        assert event_recorder.has_change_event_occurred(
            csp_subarray_sim,
            "obsState",
            ObsState.EMPTY,
        )
        assert event_recorder.has_change_event_occurred(
            mccs_subarray_sim,
            "obsState",
            ObsState.EMPTY,
        )

        assert event_recorder.has_change_event_occurred(
            central_node_low.central_node,
            "longRunningCommandResult",
            (message[0], str(ResultCode.OK.value)),
        )

        assert central_node_low.subarray_node.obsState == ObsState.EMPTY

        # Setting Assigned Resources empty
        assigned_resources_json_empty = prepare_json_args_for_commands(
            "AssignedResources_low_empty", command_input_factory
        )

        mccs_subarray_sim.SetDirectassignedResources(
            assigned_resources_json_empty
        )

        assigned_resources_attribute_value = (
            central_node_low.subarray_node.assignedResources
        )

        assigned_resources = json.loads(assigned_resources_attribute_value[0])
        assert assigned_resources["subarray_beam_ids"] == []
        assert assigned_resources["station_beam_ids"] == []
        assert assigned_resources["station_ids"] == []
        assert assigned_resources["apertures"] == []
        assert assigned_resources["channels"] == [0]
