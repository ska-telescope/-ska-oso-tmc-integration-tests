import pytest
from pytest_bdd import given, scenario, then, when
from ska_control_model import ObsState
from tango import DevState

from tests.resources.test_harness.helpers import (
    prepare_json_args_for_centralnode_commands,
    prepare_json_args_for_commands,
)
from tests.resources.test_harness.utils.enums import SimulatorDeviceType


@pytest.mark.SKA_low
@scenario(
    "../features/check_configure_command.feature",
    "Successful Configuration of Low Telescope Subarray in TMC",
)
def test_tmc_configure_command():
    """BDD test scenario for verifying successful execution of
    the Low Configure command in a TMC."""


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


@given("a subarray in the IDLE obsState")
def given_subarray_in_idle(
    command_input_factory,
    central_node_low,
    event_recorder,
    simulator_factory,
):
    """Set up a subarray in the IDLE obsState."""
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


@when("I configure it for a scan")
def send_configure(
    command_input_factory,
    subarray_node_low,
):
    """Send a Configure command to the subarray."""
    configure_input_json = prepare_json_args_for_commands(
        "configure_low", command_input_factory
    )
    subarray_node_low.execute_transition("Configure", configure_input_json)


@then("the subarray must be in the READY obsState")
def check_configure_completion(
    subarray_node_low,
    event_recorder,
    simulator_factory,
):
    """Verify that the subarray is in the READY obsState."""
    csp_subarray_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.LOW_CSP_DEVICE
    )
    sdp_subarray_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.LOW_SDP_DEVICE
    )
    mccs_subarray_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.MCCS_SUBARRAY_DEVICE
    )
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
        subarray_node_low.subarray_node,
        "obsState",
        ObsState.READY,
    )
