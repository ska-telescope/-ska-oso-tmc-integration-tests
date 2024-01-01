"""Test module to test TMC-CSP End functionality."""
import json
import logging

import pytest
from pytest_bdd import given, parsers, scenario, then, when
from ska_control_model import ObsState
from tango import DevState

from tests.resources.test_harness.helpers import (
    prepare_json_args_for_centralnode_commands,
    prepare_json_args_for_commands,
)

LOGGER = logging.getLogger(__name__)

@pytest.mark.skip
@pytest.mark.real_csp
@scenario(
    "../features/tmc_csp/tmc_csp_endscan.feature",
    "End configure from CSP Subarray using TMC",
)
def test_tmc_csp_endscan_functionality():
    """
    Test case to verify TMC-CSP observation End functionality
    """


@given("the telescope is in ON state")
def check_telescope_is_in_on_state(central_node_mid, event_recorder):
    """Ensure telescope is in ON state."""
    if central_node_mid.telescope_state != "ON":
        central_node_mid.wait.set_wait_for_csp_master_to_become_off()
        central_node_mid.csp_master.adminMode = 0
        central_node_mid.wait.wait(500)
        central_node_mid.move_to_on()
    event_recorder.subscribe_event(
        central_node_mid.central_node, "telescopeState"
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.central_node,
        "telescopeState",
        DevState.ON,
        lookahead=15,
    )


@given(parsers.parse("TMC subarray <subarray_id> is in Scanning ObsState"))
def move_subarray_node_to_scanning_obsstate(
    central_node_mid, event_recorder, command_input_factory, subarray_id
):
    """Move TMC Subarray to READY obsstate."""
    central_node_mid.set_subarray_id(subarray_id)
    assign_input_json = prepare_json_args_for_centralnode_commands(
        "assign_resources_mid", command_input_factory
    )
    # Create json for AssignResources commands with requested subarray_id
    assign_input = json.loads(assign_input_json)
    assign_input["subarray_id"] = int(subarray_id)
    central_node_mid.perform_action(
        "AssignResources", json.dumps(assign_input)
    )

    event_recorder.subscribe_event(central_node_mid.subarray_node, "obsState")
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.IDLE,
        lookahead=20,
    )
    configure_input_json = prepare_json_args_for_commands(
        "configure_mid", command_input_factory
    )
    central_node_mid.subarray_node.Configure(configure_input_json)
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.READY,
        lookahead=20,
    )

    scan_input_json = prepare_json_args_for_commands(
        "configure_mid", command_input_factory
    )
    central_node_mid.subarray_node.Configure(scan_input_json)
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.SCANNING,
        lookahead=20,
    )


@when(parsers.parse("I issue the Endscan command to the TMC subarray {subarray_id}"))
def invoke_endscan_command(central_node_mid):
    """Invoke Endscan command."""
    central_node_mid.end_observation()


@then(parsers.parse("the CSP subarray transitions to ObsState READY"))
def check_if_csp_subarray_moved_to_idle_obsstate(
    central_node_mid, event_recorder
):
    """Ensure CSP subarray is moved to READY obsstate"""
    event_recorder.subscribe_event(
        central_node_mid.subarray_devices["csp_subarray"], "obsState"
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_devices["csp_subarray"],
        "obsState",
        ObsState.READY,
    )


@then(
    parsers.parse(
        "the TMC subarray {subarray_id} transitions to ObsState READY"
    )
)
def check_if_tmc_subarray_moved_to_ready_obsstate(
    central_node_mid, event_recorder
):
    """Ensure TMC Subarray is moved to READY obsstate"""
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.READY,
        lookahead=20,
    )
