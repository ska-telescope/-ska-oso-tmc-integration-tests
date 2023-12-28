"""Test module for TMC-CSP AssignResources functionality"""
import json

import pytest
from pytest_bdd import given, parsers, scenario, then, when
from ska_control_model import ObsState
from tango import DevState


@pytest.mark.real_csp_mid
@scenario(
    "../features/tmc_csp/test_tmc_csp_assignresources.feature",
    "Assign resources to CSP subarray using TMC",
)
def test_assignresources_command():
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


@given(parsers.parse("TMC subarray {subarray_id} is in EMPTY ObsState"))
def subarray_in_empty_obsstate(central_node_mid, event_recorder, subarray_id):
    """Checks if SubarrayNode's obsState attribute value is EMPTY"""
    central_node_mid.set_subarray_id(int(subarray_id))
    event_recorder.subscribe_event(central_node_mid.subarray_node, "obsState")
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node, "obsState", ObsState.EMPTY
    )


@when(
    parsers.parse(
        "I assign resources with {receptors}to TMC subarray {subarray_id}"
    )
)
def invoke_assignresources(
    central_node_mid, event_recorder, subarray_id, receptors
):
    """Invokes AssignResources command on TMC"""
    assign_input = json.loads(central_node_mid.assign_input)
    assign_input["subarray_id"] = int(subarray_id)
    central_node_mid.perform_action(
        "AssignResources", json.dumps(assign_input)
    )


@then(
    parsers.parse("CSP subarray {subarray_id} transitioned to ObsState IDLE")
)
def csp_subarray_idle(central_node_mid, event_recorder, subarray_id):
    """Checks if Csp Subarray's obsState attribute value is IDLE"""
    csp_subarray = str(
        central_node_mid.subarray_devices.get("csp_subarray")
    ).split("/")
    csp_subarray_instance = csp_subarray[-1][-2]
    assert csp_subarray_instance == subarray_id
    event_recorder.subscribe_event(
        central_node_mid.subarray_devices["csp_subarray"], "obsState"
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_devices["csp_subarray"],
        "obsState",
        ObsState.IDLE,
    )


@then(
    parsers.parse("TMC subarray {subarray_id} transitioned to ObsState IDLE")
)
def tmc_subarray_idle(central_node_mid, event_recorder, subarray_id):
    """Checks if SubarrayNode's obsState attribute value is IDLE"""
    subarray = str(central_node_mid.subarray_node).split("/")
    subarray_instance = subarray[-1][-2]
    assert subarray_instance == subarray_id
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node, "obsState", ObsState.IDLE
    )


@then(
    parsers.parse(
        "correct resources {receptors} are assigned to"
        + " TMC subarray {subarray_id}"
    )
)
def resources_assigned_to_subarray(
    central_node_mid, event_recorder, receptors, subarray_id
):
    """Checks if correct ressources are assigned to Subarray"""
    if int(subarray_id) <= 9:
        id = f"{subarray_id:02d}"
        cbf_subarray = f"mid_csp_cbf/sub_elt/subarray_{id}"
    else:
        cbf_subarray = f"mid_csp_cbf/sub_elt/subarray_{subarray_id}"
    event_recorder.subscribe_event(cbf_subarray, "assignedResources")
    event_recorder.subscribe_event(
        central_node_mid.subarray_node, "assignedResources"
    )
    assert event_recorder.has_change_event_occurred(
        cbf_subarray,
        "assignedResources",
        receptors,
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "assignedResources",
        receptors,
    )
