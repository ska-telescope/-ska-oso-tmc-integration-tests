"""Test module for TMC-CSP ReleaseResources functionality"""
import json

import pytest
from pytest_bdd import given, parsers, scenario, then, when
from ska_control_model import ObsState
from tango import DevState


@pytest.mark.real_csp_mid
@scenario(
    "../features/tmc_csp/test_tmc_csp_releaseresources.feature",
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
def subarray_in_idle_obsstate(central_node_mid, event_recorder, subarray_id):
    """Checks if SubarrayNode's obsState attribute value is IDLE"""
    central_node_mid.set_subarray_id(int(subarray_id))
    event_recorder.subscribe_event(central_node_mid.subarray_node, "obsState")
    assign_input = json.loads(central_node_mid.assign_input)
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
def invoke_releaseresources(central_node_mid, event_recorder, subarray_id):
    """Invokes ReleaseResources command on TMC"""
    release_input = json.loads(central_node_mid.release_input)
    release_input["subarray_id"] = int(subarray_id)
    central_node_mid.invoke_release_resources(json.dumps(release_input))


@then(
    parsers.parse("the CSP subarray {subarray_id} must be in EMPTY ObsState")
)
def csp_subarray_empty(central_node_mid, event_recorder, subarray_id):
    """Checks if Csp Subarray's obsState attribute value is EMPTY"""
    csp_subarray = str(
        central_node_mid.subarray_devices.get("csp_subarray")
    ).split("/")
    csp_subarray_instance = csp_subarray[-1][-2]
    assert csp_subarray_instance == subarray_id
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
    subarray = str(central_node_mid.subarray_node).split("/")
    subarray_instance = subarray[-1][-2]
    assert subarray_instance == subarray_id
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node, "obsState", ObsState.EMPTY
    )
