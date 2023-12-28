"""Test module to test TMC-CSP Configure functionality."""
import logging

import pytest
from pytest_bdd import given, scenario, then, when
from ska_control_model import ObsState
from tango import DevState

from tests.resources.test_harness.helpers import (
    prepare_json_args_for_centralnode_commands,
    prepare_json_args_for_commands,
)

LOGGER = logging.getLogger(__name__)


@pytest.mark.real_csp_mid
@scenario(
    "../features/tmc_csp/tmc_csp_configure.feature",
    "Configure a CSP subarray for a scan using TMC",
)
def test_tmc_csp_configure_functionality():
    """
    Test case to verify TMC-CSP Configure functionality
    """


@given("the telescope is in ON state")
def check_telescope_is_in_on_state(central_node_mid, event_recorder):
    """Ensure telescope is in ON state."""
    if central_node_mid.telescope_state != "ON":
        central_node_mid.wait.set_wait_for_csp_master_to_become_off()
        central_node_mid.csp_master.adminMode = 0
        central_node_mid.wait.wait(500)
        central_node_mid.move_to_on()
    event_recorder.subscribe_event(
        central_node_mid.central_node, "telescopeState"
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.central_node,
        "telescopeState",
        DevState.ON,
        lookahead=15,
    )


@given("TMC subarray in ObsState IDLE")
def move_subarray_node_to_idle_obsstate(
    central_node_mid, event_recorder, command_input_factory
):
    """Ensure TMC Subarray in IDLE obsstate."""
    assign_input_json = prepare_json_args_for_centralnode_commands(
        "assign_resources_mid", command_input_factory
    )
    central_node_mid.perform_action("AssignResources", assign_input_json)
    event_recorder.subscribe_event(central_node_mid.subarray_node, "obsState")
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.IDLE,
        lookahead=20,
    )


@when("I issue the Configure command to the TMC subarray 1")
def invoke_configure_command(central_node_mid, command_input_factory):
    """Invoke Configure command."""
    configure_input_json = prepare_json_args_for_commands(
        "configure_mid", command_input_factory
    )
    central_node_mid.subarray_node.Configure(configure_input_json)


@then("the CSP subarray 1 transitions to ObsState READY")
def check_if_csp_subarray_moved_to_ready_obsstate(
    central_node_mid, event_recorder
):
    """Ensure CSP subarray is moved to READY obsstate"""
    event_recorder.subscribe_event(
        central_node_mid.subarray_devices["csp_subarray"], "obsState"
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_devices["csp_subarray"],
        "obsState",
        ObsState.READY,
    )


@then("the TMC subarray 1 transitions to ObsState READY")
def check_if_tmc_subarray_moved_to_ready_obsstate(
    central_node_mid, event_recorder
):
    """Ensure TMC Subarray is moved to READY obsstate"""
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.READY,
        lookahead=20,
    )


@then("CSP subarray leaf node 1 starts generating delay values")
def check_if_delay_values_are_generating(central_node_mid):
    """Check id delay model is generating."""
    delay_value = central_node_mid.csp_subarray_leaf_node.delayModel
    LOGGER.info("Delay_Values: %s", delay_value)
