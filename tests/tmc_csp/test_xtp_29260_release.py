"""Test module for TMC-CSP ReleaseResources functionality"""
import json

import pytest
from pytest_bdd import given, parsers, scenario, then, when
from ska_control_model import ObsState
from tango import DevState

from tests.resources.test_harness.helpers import (
    prepare_json_args_for_centralnode_commands,
    wait_csp_master_off,
)


@pytest.mark.tmc_csp
@scenario(
    "../features/tmc_csp/xtp_29260_release.feature",
    "Release resources from CSP subarray using TMC",
)
def test_releaseresources_command():
    """BDD test scenario for verifying successful execution of
    the AssignResources command with TMC and CSP devices for pairwise
    testing."""


@given("the telescope is in ON state")
def given_a_telescope_in_on_state(
    central_node_mid, event_recorder, simulator_factory
):
    """Checks if CentralNode's telescopeState attribute value is on."""

    event_recorder.subscribe_event(
        central_node_mid.central_node, "telescopeState"
    )
    central_node_mid.csp_master.adminMode = 0
    wait_csp_master_off()
    central_node_mid.move_to_on()
    event_recorder.subscribe_event(central_node_mid.csp_master, "State")
    event_recorder.subscribe_event(
        central_node_mid.subarray_devices["csp_subarray"], "State"
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.csp_master,
        "State",
        DevState.ON,
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_devices["csp_subarray"],
        "State",
        DevState.ON,
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.central_node,
        "telescopeState",
        DevState.ON,
    )


@given(parsers.parse("TMC subarray {subarray_id} is in IDLE ObsState"))
def subarray_in_idle_obsstate(
    central_node_mid, event_recorder, subarray_id, command_input_factory
):
    """Checks if SubarrayNode's obsState attribute value is IDLE"""
    central_node_mid.set_subarray_id(subarray_id)
    event_recorder.subscribe_event(central_node_mid.subarray_node, "obsState")
    assign_input_json = prepare_json_args_for_centralnode_commands(
        "assign_resources_mid", command_input_factory
    )
    assign_input = json.loads(assign_input_json)
    assign_input["subarray_id"] = int(subarray_id)
    central_node_mid.perform_action(
        "AssignResources", json.dumps(assign_input)
    )
    event_recorder.subscribe_event(
        central_node_mid.subarray_devices["csp_subarray"], "obsState"
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_devices["csp_subarray"],
        "obsState",
        ObsState.IDLE,
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node, "obsState", ObsState.IDLE
    )


@when(
    parsers.parse(
        "I release all resources assign to TMC subarray {subarray_id}"
    )
)
def invoke_releaseresources(
    central_node_mid, event_recorder, subarray_id, command_input_factory
):
    """Invokes ReleaseResources command on TMC"""
    release_input_json = prepare_json_args_for_centralnode_commands(
        "release_resources_mid", command_input_factory
    )
    release_input = json.loads(release_input_json)
    release_input["subarray_id"] = subarray_id
    central_node_mid.invoke_release_resources(json.dumps(release_input))


@then(
    parsers.parse("the CSP subarray {subarray_id} must be in EMPTY ObsState")
)
def csp_subarray_empty(central_node_mid, event_recorder, subarray_id):
    """Checks if Csp Subarray's obsState attribute value is EMPTY"""
    central_node_mid.set_subarray_id(subarray_id)
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_devices["csp_subarray"],
        "obsState",
        ObsState.EMPTY,
    )


@then(
    parsers.parse(
        "the TMC subarray {subarray_id} transitions to ObsState EMPTY"
    )
)
def tmc_subarray_empty(central_node_mid, event_recorder, subarray_id):
    """Checks if SubarrayNode's obsState attribute value is EMPTY"""
    central_node_mid.set_subarray_id(subarray_id)
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node, "obsState", ObsState.EMPTY
    )
