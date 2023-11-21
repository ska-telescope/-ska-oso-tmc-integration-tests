import pytest
from pytest_bdd import given, parsers, scenario, then, when
from ska_control_model import ObsState
from tango import DevState

from tests.resources.test_harness.helpers import (
    prepare_json_args_for_centralnode_commands,
    prepare_json_args_for_commands,
)
from tests.resources.test_harness.utils.enums import SimulatorDeviceType


@pytest.mark.bdd_scan
@pytest.mark.SKA_low
@scenario(
    "../features/check_scan_command.feature",
    "Successful Execution of Scan Command on Low Telescope Subarray in TMC",
)
def test_tmc_mccssln_scan_command():
    """BDD test scenario for verifying successful execution of
    the Scan command in a TMC."""


@given("a TMC")
def given_tmc(central_node_low, event_recorder):
    """Set up a TMC and ensure it is in the ON state."""
    event_recorder.subscribe_event(
        central_node_low.central_node, "telescopeState"
    )
    event_recorder.subscribe_event(central_node_low.subarray_node, "obsState")
    central_node_low.move_to_on()
    assert event_recorder.has_change_event_occurred(
        central_node_low.central_node,
        "telescopeState",
        DevState.ON,
    )
    assert event_recorder.has_change_event_occurred(
        central_node_low.subarray_node,
        "obsState",
        ObsState.EMPTY,
    )


@given("a subarray in READY obsState")
def given_subarray_in_ready(
    command_input_factory,
    central_node_low,
    subarray_node_low,
    event_recorder,
    simulator_factory,
):
    """Set up a subarray in the READY state."""
    csp_subarray_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.LOW_CSP_DEVICE
    )
    sdp_subarray_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.LOW_SDP_DEVICE
    )
    mccs_subarray_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.MCCS_SUBARRAY_DEVICE
    )
    event_recorder.subscribe_event(csp_subarray_sim, "obsState")
    event_recorder.subscribe_event(sdp_subarray_sim, "obsState")
    event_recorder.subscribe_event(mccs_subarray_sim, "obsState")
    event_recorder.subscribe_event(central_node_low.subarray_node, "obsState")
    assign_input_json = prepare_json_args_for_centralnode_commands(
        "assign_resources_low", command_input_factory
    )
    central_node_low.perform_action("AssignResources", assign_input_json)
    assert event_recorder.has_change_event_occurred(
        csp_subarray_sim,
        "obsState",
        ObsState.IDLE,
    )
    assert event_recorder.has_change_event_occurred(
        sdp_subarray_sim,
        "obsState",
        ObsState.IDLE,
    )
    assert event_recorder.has_change_event_occurred(
        mccs_subarray_sim,
        "obsState",
        ObsState.IDLE,
    )
    assert event_recorder.has_change_event_occurred(
        central_node_low.subarray_node,
        "obsState",
        ObsState.IDLE,
    )
    configure_input_json = prepare_json_args_for_commands(
        "configure_low", command_input_factory
    )
    subarray_node_low.execute_transition("Configure", configure_input_json)
    assert event_recorder.has_change_event_occurred(
        csp_subarray_sim,
        "obsState",
        ObsState.READY,
    )
    assert event_recorder.has_change_event_occurred(
        sdp_subarray_sim,
        "obsState",
        ObsState.READY,
    )
    assert event_recorder.has_change_event_occurred(
        mccs_subarray_sim,
        "obsState",
        ObsState.READY,
    )
    assert event_recorder.has_change_event_occurred(
        central_node_low.subarray_node,
        "obsState",
        ObsState.READY,
    )


@when(parsers.parse("I command it to scan for a given period"))
def send_scan(
    command_input_factory,
    subarray_node_low,
):
    """Send a Scan command to the subarray."""
    scan_input_json = prepare_json_args_for_commands(
        "scan_low", command_input_factory
    )
    subarray_node_low.execute_transition("Scan", scan_input_json)


@then("the subarray must be in the SCANNING obsState until finished")
def scan_complete(
    subarray_node_low,
    event_recorder,
    simulator_factory,
):
    """Verify that the subarray is in the SCANNING obsState."""
    csp_subarray_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.LOW_CSP_DEVICE
    )
    sdp_subarray_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.LOW_SDP_DEVICE
    )
    mccs_subarray_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.MCCS_SUBARRAY_DEVICE
    )

    event_recorder.subscribe_event(csp_subarray_sim, "obsState")
    event_recorder.subscribe_event(sdp_subarray_sim, "obsState")
    event_recorder.subscribe_event(mccs_subarray_sim, "obsState")
    event_recorder.subscribe_event(subarray_node_low.subarray_node, "obsState")
    assert event_recorder.has_change_event_occurred(
        csp_subarray_sim,
        "obsState",
        ObsState.SCANNING,
    )
    assert event_recorder.has_change_event_occurred(
        sdp_subarray_sim,
        "obsState",
        ObsState.SCANNING,
    )
    assert event_recorder.has_change_event_occurred(
        mccs_subarray_sim,
        "obsState",
        ObsState.SCANNING,
    )
    assert event_recorder.has_change_event_occurred(
        subarray_node_low.subarray_node,
        "obsState",
        ObsState.SCANNING,
    )
