"""Test TMC-SDP Abort functionality"""
import pytest
from pytest_bdd import given, parsers, scenario, then, when
from ska_control_model import ObsState
from tango import DevState

from tests.resources.test_harness.helpers import (
    prepare_json_args_for_centralnode_commands,
)


@pytest.mark.real_sdp
@scenario(
    "../features/tmc_sdp/tmc_sdp_abort.feature",
    "Abort assigning using TMC",
)
def test_tmc_sdp_abort_in_resourcing(central_node_mid):
    """
    Test case to verify TMC-SDP Abort functionality in RESOURCING obsState
    """


@given("TMC and SDP subarray busy assigning resources")
def telescope_is_in_resourcing_obsstate(
    central_node_mid, event_recorder, command_input_factory
):
    """ "A method to check if telescope in is resourcing obsSstate."""
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
        central_node_mid.subarray_devices.get("sdp_subarray"), "obsState"
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_devices.get("sdp_subarray"),
        "obsState",
        ObsState.RESOURCING,
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.RESOURCING,
    )


@when(
    parsers.parse(
        "I issued the Abort command to the TMC subarray {subarray_id}"
    )
)
@when(parsers.parse("I command it to Abort"))
def abort_is_invoked(central_node_mid, subarray_id="1"):
    """
    This method is to invoke abort command on tmc subarray
    """
    central_node_mid.set_subarray_id((int(subarray_id)))
    central_node_mid.subarray_abort()


@then(parsers.parse("the SDP subarray should go into an ABORTED obsstate"))
def sdp_subarray_is_in_aborted_obsstate(central_node_mid, event_recorder):
    """
    Method to check SDP subarray is in ABORTED obsstate
    """
    event_recorder.subscribe_event(
        central_node_mid.subarray_devices.get("sdp_subarray"), "obsState"
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_devices.get("sdp_subarray"),
        "obsState",
        ObsState.ABORTED,
    )


@then(
    parsers.parse(
        "the TMC subarray <subarray_id> transitions to ABORTED ObsState"
    )
)
@then(parsers.parse("the TMC subarray obsState transitions to ABORTED"))
def tmc_subarray_is_in_aborted_obsstate(central_node_mid, event_recorder):
    """
    Method to check TMC subarray is in ABORTED obsstate
    """
    event_recorder.subscribe_event(central_node_mid.subarray_node, "obsState")
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.ABORTED,
    )


@pytest.mark.real_sdp
@scenario(
    "../features/tmc_sdp/tmc_sdp_abort.feature",
    "TMC executes an Abort on SDP subarray while subarray completes"
    + " configuration",
)
def test_tmc_sdp_abort_in_idle(central_node_mid):
    """
    Test case to verify TMC-SDP Abort functionality in IDLE obsState
    """


@given(parsers.parse("TMC and SDP subarray is in {obsstate} ObsState"))
def telescope_is_in_idle_obsstate(
    central_node_mid, event_recorder, command_input_factory, obsstate
):
    """ "A method to check if telescope in is IDLE obsSstate."""
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
        central_node_mid.subarray_devices.get("sdp_subarray"), "obsState"
    )
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
