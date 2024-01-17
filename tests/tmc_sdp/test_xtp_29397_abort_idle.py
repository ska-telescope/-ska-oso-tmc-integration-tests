"""Test TMC-SDP Abort functionality in IDLE obstate"""
import pytest
from pytest_bdd import given, parsers, scenario, then, when
from ska_control_model import ObsState
from tango import DevState

from tests.resources.test_harness.helpers import (
    prepare_json_args_for_centralnode_commands,
)


@pytest.mark.tmc_sdp
@scenario(
    "../features/tmc_sdp/xtp_29397_abort_idle.feature",
    "TMC executes an Abort on SDP subarray while subarray completes"
    + " configuration",
)
def test_tmc_sdp_abort_in_idle(central_node_mid):
    """
    Test case to verify TMC-SDP Abort functionality in IDLE obsState
    """


@given("the telescope is in ON state")
def telescope_is_in_on_state(central_node_mid, event_recorder):
    """
    This method checks if the telescope is in ON state
    """
    central_node_mid.move_to_on()
    event_recorder.subscribe_event(
        central_node_mid.central_node, "telescopeState"
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.central_node,
        "telescopeState",
        DevState.ON,
    )


@given(
    parsers.parse(
        "TMC and SDP subarray {subarray_id} is in {obsstate} ObsState"
    )
)
def telescope_is_in_idle_obsstate(
    central_node_mid,
    event_recorder,
    command_input_factory,
    obsstate,
    subarray_id,
):
    """ "A method to check if telescope in is IDLE obsSstate."""
    central_node_mid.set_subarray_id(subarray_id)
    assign_input_json = prepare_json_args_for_centralnode_commands(
        "assign_resources_mid", command_input_factory
    )
    central_node_mid.store_resources(assign_input_json)
    event_recorder.subscribe_event(
        central_node_mid.subarray_devices.get("sdp_subarray"), "obsState"
    )
    event_recorder.subscribe_event(central_node_mid.subarray_node, "obsState")
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_devices.get("sdp_subarray"),
        "obsState",
        ObsState[obsstate],
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState[obsstate],
    )


@when(
    parsers.parse(
        "I issued the Abort command to the TMC subarray {subarray_id}"
    )
)
def invoke_abort(central_node_mid, subarray_id):
    """
    This method invokes abort command on tmc subarray
    """
    central_node_mid.set_subarray_id(subarray_id)
    central_node_mid.subarray_abort()


@then(
    parsers.parse(
        "the SDP subarray {subarray_id} transitions to ObsState ABORTED"
    )
)
def sdp_subarray_is_in_aborted_obsstate(
    central_node_mid, event_recorder, subarray_id
):
    """
    Method to check SDP subarray is in ABORTED obsstate
    """
    central_node_mid.set_subarray_id(subarray_id)
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_devices.get("sdp_subarray"),
        "obsState",
        ObsState.ABORTED,
    )


@then(
    parsers.parse(
        "the TMC subarray {subarray_id} transitions to ObsState ABORTED"
    )
)
def tmc_subarray_is_in_aborted_obsstate(
    central_node_mid, event_recorder, subarray_id
):
    """
    Method to check if TMC subarray is in ABORTED obsstate
    """
    central_node_mid.set_subarray_id(subarray_id)
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.ABORTED,
    )
