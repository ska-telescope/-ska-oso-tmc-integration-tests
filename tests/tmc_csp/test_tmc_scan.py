"""Test module for TMC-CSP ReleaseResources functionality"""

import pytest
from pytest_bdd import given, parsers, scenario, then, when
from ska_control_model import ObsState
from tango import DevState

from tests.resources.test_harness.helpers import (
    prepare_json_args_for_centralnode_commands,
    prepare_json_args_for_commands,
    wait_csp_master_off,
)


@pytest.mark.real_csp_mid
@scenario(
    "../features/tmc_csp/tmc_csp_scan.feature",
    "TMC executes a Scan command on CSP subarray.",
)
def test_scan_command():
    """BDD test scenario for verifying successful execution of
    the Scan command with TMC and CSP devices for pairwise
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


@given(parsers.parse("TMC subarray {subarray_id} is in READY ObsState"))
def subarray_in_ready_obsstate(
    central_node_mid,
    event_recorder,
    subarray_id,
    command_input_factory,
    subarray_node,
):
    """Checks if SubarrayNode's obsState attribute value is READY"""
    central_node_mid.set_subarray_id(int(subarray_id))
    event_recorder.subscribe_event(central_node_mid.subarray_node, "obsState")
    event_recorder.subscribe_event(
        central_node_mid.subarray_devices.get("csp_subarray"), "obsState"
    )
    assign_input_json = prepare_json_args_for_centralnode_commands(
        "assign_resources_mid", command_input_factory
    )

    central_node_mid.store_resources(assign_input_json)

    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_devices.get("csp_subarray"),
        "obsState",
        ObsState.IDLE,
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.IDLE,
    )

    configure_input_json = prepare_json_args_for_commands(
        "configure_mid", command_input_factory
    )
    central_node_mid.subarray_node.Configure(configure_input_json)
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node, "obsState", ObsState.READY
    )
    # subarray_node.force_change_of_obs_state("READY")


@when(
    parsers.parse("I issue the scan command to the TMC subarray {subarray_id}")
)
def invoke_scan(
    central_node_mid, event_recorder, subarray_id, command_input_factory
):
    """Invokes ReleaseResources command on TMC"""
    scan_input_json = prepare_json_args_for_commands(
        "scan_mid", command_input_factory
    )
    central_node_mid.subarray_node.Scan(scan_input_json)


@then(parsers.parse(" the CSP subarray transitions to ObsState SCANNING"))
def csp_subarray_scanning(central_node_mid, event_recorder, subarray_id):
    """Checks if Csp Subarray's obsState attribute value is SCANNING"""
    central_node_mid.set_subarray_id(int(subarray_id))
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_devices["csp_subarray"],
        "obsState",
        ObsState.SCANNING,
    )


@then(
    parsers.parse(
        "the TMC subarray <subarray_id> transitions to ObsState SCANNING"
    )
)
def tmc_subarray_scanning(central_node_mid, event_recorder, subarray_id):
    """Checks if SubarrayNode's obsState attribute value is SCANNING"""
    central_node_mid.set_subarray_id(int(subarray_id))
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node, "obsState", ObsState.SCANNING
    )


@then(
    parsers.parse(
        "the CSP subarray ObsState transitions to READY after the"
        + " scan duration elapsed"
    )
)
def tmc_subarray_ObsState(central_node_mid, event_recorder, subarray_id):
    """Checks if SubarrayNode's obsState attribute value is READY"""
    central_node_mid.set_subarray_id(int(subarray_id))
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node, "obsState", ObsState.READY
    )


@then(
    parsers.parse(
        "the CSP subarray ObsState transitions to READY after"
        + " the scan duration elapsed"
    )
)
def tmc_subarray_ready(central_node_mid, event_recorder, subarray_id):
    """Checks if SubarrayNode's obsState attribute value is EMPTY"""
    central_node_mid.set_subarray_id(int(subarray_id))
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node, "obsState", ObsState.READY
    )
