"""Test module for TMC-CSP AssignResources functionality"""
import time

import pytest
from pytest_bdd import given, parsers, scenario, then, when
from ska_control_model import ObsState
from tango import DevState

from tests.resources.test_harness.helpers import (
    check_assigned_resources,
    get_master_device_simulators,
)


@pytest.mark.real_csp_mid
@scenario(
    "../features/test_harness/test_tmc_csp_assignresources.feature",
    "Assign resources to CSP subarray using TMC",
)
def test_assignresources_command():
    """BDD test scenario for verifying successful execution of
    the AssignResources command with TMC and CSP devices for pairwise
    testing."""


@given("Given the telescope is in ON state")
def given_a_telescope_in_on_state(
    central_node_mid, event_recorder, simulator_factory
):
    """Checks if CentralNode's telescopeState attribute value is on."""
    (
        _,
        sdp_master_sim,
        dish_master_sim_1,
        dish_master_sim_2,
    ) = get_master_device_simulators(simulator_factory)

    assert central_node_mid.central_node.ping() > 0
    assert central_node_mid.sdp_master.ping() > 0
    assert central_node_mid.subarray_devices["sdp_subarray"].ping() > 0
    assert sdp_master_sim.ping() > 0
    assert dish_master_sim_1.ping() > 0
    assert dish_master_sim_2.ping() > 0
    event_recorder.subscribe_event(
        central_node_mid.central_node, "telescopeState"
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.central_node,
        "telescopeState",
        DevState.STANDBY,
    )
    central_node_mid.csp_master.adminMode = 0
    central_node_mid.wait.set_wait_for_csp_master_to_become_online()
    time.sleep(30)  # Yes, This sleep will be removed.
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
def subarray_in_empty_obsstate(central_node_mid, event_recorder):
    """Checks if SubarrayNode's obsState attribute value is EMPTY"""
    event_recorder.subscribe_event(central_node_mid.subarray_node, "obsState")
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node, "obsState", ObsState.EMPTY
    )


@when(
    parsers.parse(
        "I assign resources with {receptors}to TMC subarray {subarray_id}"
    )
)
def invoke_assignresources(central_node_mid, event_recorder):
    """Invokes AssignResources command on TMC"""
    central_node_mid.store_resources(central_node_mid.assign_input)


@then(
    parsers.parse("CSP subarray {subarray_id} transitioned to ObsState IDLE")
)
def csp_subarray_idle(central_node_mid, event_recorder):
    """Checks if Csp Subarray's obsState attribute value is IDLE"""
    event_recorder.subscribe_event(central_node_mid.csp_subarray, "obsState")
    assert event_recorder.has_change_event_occurred(
        central_node_mid.csp_subarray, "obsState", ObsState.IDLE
    )


@then(
    parsers.parse("TMC subarray {subarray_id} transitioned to ObsState IDLE")
)
def tmc_subarray_idle(central_node_mid, event_recorder):
    """Checks if SubarrayNode's obsState attribute value is IDLE"""
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node, "obsState", ObsState.IDLE
    )


@then(
    parsers.parse(
        "correct resources {receptors} are assigned to"
        + " TMC subarray {subarray_id}"
    )
)
def resources_assigned_to_subarray(central_node_mid, event_recorder):
    """Checks if correct ressources are assigned to Subarray"""
    event_recorder.subscribe_event(
        central_node_mid.subarray_node, "assignedResources"
    )
    assert check_assigned_resources(
        central_node_mid.subarray_node,
        ("SKA001", "SKA002", "SKA003", "SKA004"),
    )
