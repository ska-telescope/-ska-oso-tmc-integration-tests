"""Test TMC-CSP Abort functionality in Configuring obstate"""

import pytest
from pytest_bdd import given, parsers, scenario, then, when
from ska_control_model import ObsState
from tango import DevState

from tests.resources.test_harness.helpers import (
    prepare_json_args_for_centralnode_commands,
    prepare_json_args_for_commands,
)


@pytest.mark.tmc_csp
@scenario(
    "../features/tmc_csp/xtp_29838_abort_configuring.feature",
    "Abort configuring CSP using TMC",
)
def test_tmc_csp_abort_in_configuring():
    """
    Test case to verify TMC-CSP Abort functionality in CONFIGURING obsState
    """


@given("the telescope is in ON state")
def given_a_telescope_in_on_state(central_node_mid, event_recorder):
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


@given(
    parsers.parse(
        "the TMC subarray {subarray_id} and CSP subarray {subarray_id}",
        " is busy in configuring",
    )
)
def subarray_is_in_configuring_obsstate(
    central_node_mid,
    event_recorder,
    command_input_factory,
    subarray_node,
    subarray_id,
):
    """A method to check if telescope in is CONFIGURING obsSstate."""
    central_node_mid.set_subarray_id(subarray_id)
    central_node_mid.move_to_on()
    event_recorder.subscribe_event(
        central_node_mid.central_node, "telescopeState"
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.central_node,
        "telescopeState",
        DevState.ON,
    )
    assign_input_json = prepare_json_args_for_centralnode_commands(
        "assign_resources_mid", command_input_factory
    )
    central_node_mid.store_resources(assign_input_json)
    event_recorder.subscribe_event(
        subarray_node.subarray_devices.get("csp_subarray"), "obsState"
    )
    event_recorder.subscribe_event(subarray_node.subarray_node, "obsState")
    assert event_recorder.has_change_event_occurred(
        subarray_node.subarray_devices.get("csp_subarray"),
        "obsState",
        ObsState.IDLE,
    )
    assert event_recorder.has_change_event_occurred(
        subarray_node.subarray_node,
        "obsState",
        ObsState.IDLE,
    )
    input_json = prepare_json_args_for_commands(
        "configure_mid", command_input_factory
    )
    subarray_node.execute_transition("Configure", input_json)
    assert event_recorder.has_change_event_occurred(
        subarray_node.subarray_devices["csp_subarray"],
        "obsState",
        ObsState.CONFIGURING,
    )
    assert event_recorder.has_change_event_occurred(
        subarray_node.subarray_node,
        "obsState",
        ObsState.CONFIGURING,
    )


@when(
    parsers.parse(
        "I issued the Abort command to the TMC subarray {subarray_id}"
    )
)
def abort_is_invoked(subarray_node, subarray_id):
    """
    This method invokes abort command on tmc subarray.
    """
    subarray_node.set_subarray_id(subarray_id)
    subarray_node.abort_subarray()


@then(
    parsers.parse(
        "the CSP subarray {subarray_id} transitions to ObsState ABORTED"
    )
)
def csp_subarray_is_in_aborted_obsstate(
    subarray_node, event_recorder, subarray_id
):
    """
    Method to check CSP subarray is in ABORTED obsstate
    """
    subarray_node.set_subarray_id(subarray_id)
    assert event_recorder.has_change_event_occurred(
        subarray_node.subarray_devices.get("csp_subarray"),
        "obsState",
        ObsState.ABORTED,
    )


@then(
    parsers.parse(
        "the TMC subarray {subarray_id} transitions to ObsState ABORTED"
    )
)
def tmc_subarray_is_in_aborted_obsstate(
    subarray_node, event_recorder, subarray_id
):
    """
    Method to check if TMC subarray is in ABORTED obsstate
    """
    subarray_node.set_subarray_id(subarray_id)
    assert event_recorder.has_change_event_occurred(
        subarray_node.subarray_node,
        "obsState",
        ObsState.ABORTED,
    )
