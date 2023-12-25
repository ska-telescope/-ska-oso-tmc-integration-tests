"""Test TMC-SDP ReleaseResources functionality"""
import logging

import pytest
from pytest_bdd import given, parsers, scenario, then, when
from ska_control_model import ObsState
from ska_ser_logging import configure_logging
from tango import DevState

from tests.resources.test_harness.helpers import (
    prepare_json_args_for_centralnode_commands,
)

configure_logging(logging.DEBUG)
LOGGER = logging.getLogger(__name__)


@pytest.mark.real_sdp
@scenario(
    "../features/sdp_tmc_release_resources.feature",
    "Release resources from SDP Subarray using TMC",
)
def test_tmc_sdp_release_resources():
    """
    Test case to verify TMC-SDP ReleaseResources functionality
    """


@given("a TMC and SDP")
def given_a_tmc():
    """A method to define TMC and SDP."""


@given(parsers.parse("a subarray {subarray_id} in the IDLE obsState"))
def telescope_is_in_idle_state(
    central_node_mid, event_recorder, command_input_factory
):
    """ "A method to move telescope into the IDLE state."""
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


@when(
    parsers.parse("I release all resources assigned to subarray {subarray_id}")
)
def release_resources_to_subarray(central_node_mid, command_input_factory):
    """Method to release resources to subarray."""
    release_input_json = prepare_json_args_for_centralnode_commands(
        "release_resources_mid", command_input_factory
    )
    central_node_mid.invoke_release_resources(release_input_json)


@then(
    parsers.parse("the SDP subarray {subarray_id} must be in EMPTY obsState")
)
def check_sdp_is_in_empty_obsstate(central_node_mid, event_recorder):
    """Method to check SDP is in EMPTY obsstate"""
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_devices.get("sdp_subarray"),
        "obsState",
        ObsState.EMPTY,
    )


@then(
    parsers.parse("TMC subarray {subarray_id} obsState transitions to EMPTY")
)
def check_tmc_is_in_idle_obsstate(central_node_mid, event_recorder):
    """Method to check TMC is is in EMPTY obsstate."""
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.EMPTY,
    )
