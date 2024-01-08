"""Test TMC-SDP Abort functionality in Configuring obstate"""
import pytest
from pytest_bdd import given, scenario, then, when
from ska_control_model import ObsState
from tango import DevState

from tests.resources.test_harness.helpers import (
    prepare_json_args_for_centralnode_commands,
    prepare_json_args_for_commands,
)


@pytest.mark.skip
@pytest.mark.tmc_sdp
@scenario(
    "../features/tmc_sdp/xtp_29398_abort_configuring.feature",
    "Abort configuring SDP using TMC",
)
def test_tmc_sdp_abort_in_configuring():
    """
    Test case to verify TMC-SDP Abort functionality in CONFIGURING obsState
    """


@given("TMC subarray busy configuring")
def telescope_is_in_configuring_obsstate(
    central_node_mid,
    event_recorder,
    command_input_factory,
    subarray_node,
):
    """ "A method to check if telescope in is CONFIGURING obsSstate."""
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
    event_recorder.subscribe_event(central_node_mid.subarray_node, "obsState")
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_devices.get("sdp_subarray"),
        "obsState",
        ObsState.IDLE,
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.IDLE,
    )
    input_json = prepare_json_args_for_commands(
        "configure_mid", command_input_factory
    )
    subarray_node.execute_transition("Configure", input_json)
    assert event_recorder.has_change_event_occurred(
        subarray_node.subarray_devices["sdp_subarray"],
        "obsState",
        ObsState.CONFIGURING,
    )
    assert event_recorder.has_change_event_occurred(
        subarray_node.subarray_node,
        "obsState",
        ObsState.CONFIGURING,
    )


@when("I command it to Abort")
def abort_is_invoked(central_node_mid):
    """
    This method invokes abort command on tmc subarray
    """
    central_node_mid.subarray_abort()


@then("the SDP subarray should go into an ABORTED obsstate")
def sdp_subarray_is_in_aborted_obsstate(central_node_mid, event_recorder):
    """
    Method to check SDP subarray is in ABORTED obsstate
    """
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_devices.get("sdp_subarray"),
        "obsState",
        ObsState.ABORTED,
    )


@then("the TMC subarray obsState transitions to ABORTED")
def tmc_subarray_is_in_aborted_obsstate(central_node_mid, event_recorder):
    """
    Method to check if TMC subarray is in ABORTED obsstate
    """
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.ABORTED,
    )
