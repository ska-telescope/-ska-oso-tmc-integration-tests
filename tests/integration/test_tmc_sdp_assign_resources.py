"""Test TMC-SDP AssignResources functionality"""
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
@pytest.mark.test
@scenario(
    "../features/sdp_tmc_assign_resources.feature",
    "Assign resources to SDP subarray using TMC",
)
def test_tmc_sdp_assign_resources():
    """
    Test case to verify TMC-SDP AssignResources functionality
    """


@given("the Telescope is in ON state")
def telescope_is_in_on_state(central_node_mid, event_recorder):
    """ "A method to move telescope into the ON state."""
    central_node_mid.move_to_on()
    event_recorder.subscribe_event(
        central_node_mid.central_node, "telescopeState"
    )
    LOGGER.info(f"State is: {central_node_mid.central_node.telescopeState}")
    assert central_node_mid.central_node.telescopeState == DevState.ON
    assert event_recorder.has_change_event_occurred(
        central_node_mid.central_node,
        "telescopeState",
        DevState.ON,
    )


@given(parsers.parse("the subarray {subarray_id} obsState is EMPTY"))
def subarray_is_in_empty_obsstate(event_recorder, central_node_mid):
    """Method to check subarray is in EMPTY obstate"""
    event_recorder.subscribe_event(central_node_mid.subarray_node, "obsState")
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.EMPTY,
    )


@when(
    parsers.parse(
        "I assign resources with the {receptors} to the subarray {subarray_id}"
    )
)
def assign_resources_to_subarray(central_node_mid, command_input_factory):
    """Method to assign resources to subarray."""
    assign_input_json = prepare_json_args_for_centralnode_commands(
        "assign_resources_mid", command_input_factory
    )
    central_node_mid.store_resources(assign_input_json)


@then(parsers.parse("the sdp subarray {subarray_id} obsState is IDLE"))
def check_sdp_is_in_idle_obsstate(central_node_mid, event_recorder):
    """Method to check SDP is in IDLE obsstate"""
    event_recorder.subscribe_event(
        central_node_mid.subarray_devices.get("sdp_subarray"), "obsState"
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_devices.get("sdp_subarray"),
        "obsState",
        ObsState.IDLE,
    )


@then(
    parsers.parse(
        "the TMC subarray {subarray_id} obsState is transitioned to IDLE"
    )
)
def check_tmc_is_in_idle_obsstate(central_node_mid, event_recorder):
    """Method to check TMC is is in IDLE obsstate."""
    event_recorder.subscribe_event(central_node_mid.subarray_node, "obsState")
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.IDLE,
    )


@then(
    parsers.parse(
        "the correct resources {receptors} are assigned to sdp subarray \
            and TMC subarray"
    )
)
def check_assign_resources_to_tmc(central_node_mid, receptors):
    central_node_mid.subarray_node.assignedResources = receptors
