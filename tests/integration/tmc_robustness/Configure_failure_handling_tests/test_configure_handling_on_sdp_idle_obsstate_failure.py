import pytest
from pytest_bdd import given, parsers, scenario, then, when
from ska_control_model import ObsState
from ska_tango_base.commands import ResultCode

# from ska_tango_testing.mock.placeholders import Anything
from tango import DevState

from tests.resources.test_harness.helpers import (
    get_device_simulators,
    prepare_json_args_for_centralnode_commands,
    prepare_json_args_for_commands,
)
from tests.resources.test_harness.utils.enums import SimulatorDeviceType


@pytest.mark.bdd_configure
@pytest.mark.SKA_mid
@scenario(
    "../features/configure_sdp_subarray_failure_scenario.feature",
    "TMC behavior when SDP Subarray Configure raises exception",
)
def test_configure_handling_on_sdp_subarray_obsstate_idle_failure(
    central_node_mid, subarray_node, event_recorder, simulator_factory
):
    """
    Test to verify TMC failure handling when Configure command fails on
    SDP Subarray. Configure completes on CSP Subarray and
    it transtions to obsState READY.
    Whereas SDP Subarray raises exception and transitions
    to obsState IDLE. As a handling End is invoked on CSP Subarray.
    CSP Subarray then moves to obsState IDLE.
    SubarrayNode aggregates obsStates of the lower Subarrays
    and transitions to obsState IDLE.
    Glossary:
    - "central_node_mid": fixture for a TMC CentralNode Mid under test
    which provides simulated master devices
    - "subarray_node": fixture for a TMC SubarrayNode under test
    which provides simulated subarray and master devices
    - "event_recorder": fixture for a MockTangoEventCallbackGroup
    for validating the subscribing and receiving events.
    - "simulator_factory": fixture for creating simulator devices for
    mid Telescope respectively.
    """


@given("a TMC")
def given_tmc(central_node_mid, subarray_node, event_recorder):
    event_recorder.subscribe_event(
        central_node_mid.central_node, "telescopeState"
    )
    event_recorder.subscribe_event(subarray_node.subarray_node, "obsState")
    central_node_mid.move_to_on()
    assert event_recorder.has_change_event_occurred(
        central_node_mid.central_node,
        "telescopeState",
        DevState.ON,
    )
    assert event_recorder.has_change_event_occurred(
        subarray_node.subarray_node,
        "obsState",
        ObsState.EMPTY,
    )


@given(parsers.parse("the resources are assigned to TMC SubarrayNode"))
def given_tmc_subarray_assign_resources(
    central_node_mid,
    subarray_node,
    event_recorder,
    simulator_factory,
    command_input_factory,
):
    csp_sim, sdp_sim, _, _ = get_device_simulators(simulator_factory)
    event_recorder.subscribe_event(csp_sim, "obsState")
    event_recorder.subscribe_event(sdp_sim, "obsState")
    event_recorder.subscribe_event(subarray_node.subarray_node, "obsState")
    event_recorder.subscribe_event(
        central_node_mid.central_node, "longRunningCommandResult"
    )

    assign_input_json = prepare_json_args_for_centralnode_commands(
        "assign_resources_mid", command_input_factory
    )
    invalid_receiptor_json = prepare_json_args_for_commands(
        "invalid_receiptor", command_input_factory
    )
    _, unique_id = central_node_mid.perform_action(
        "AssignResources", assign_input_json
    )
    sdp_sim.SetDirectreceiveAddresses(invalid_receiptor_json)
    assert event_recorder.has_change_event_occurred(
        subarray_node.subarray_node,
        "obsState",
        ObsState.IDLE,
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.central_node,
        "longRunningCommandResult",
        (unique_id[0], str(ResultCode.OK.value)),
    )


@given(
    parsers.parse(
        "the TMC SubarrayNode {subarray_id} Configure is in progress"
    )
)
def given_tmc_subarray_configure_is_in_progress(
    subarray_node, event_recorder, simulator_factory, command_input_factory
):
    csp_sim, sdp_sim, _, _ = get_device_simulators(simulator_factory)
    event_recorder.subscribe_event(csp_sim, "obsState")
    event_recorder.subscribe_event(sdp_sim, "obsState")
    event_recorder.subscribe_event(subarray_node.subarray_node, "obsState")
    event_recorder.subscribe_event(
        subarray_node.subarray_node, "longRunningCommandResult"
    )

    # Induce fault on SDP Subarry so that it raises exception and
    # returns to the obsState IDLE
    configure_input_json = prepare_json_args_for_commands(
        "configure_with_invalid_scan_type", command_input_factory
    )
    pytest.command_result = subarray_node.execute_transition(
        "Configure", configure_input_json
    )
    assert event_recorder.has_change_event_occurred(
        subarray_node.subarray_node,
        "obsState",
        ObsState.CONFIGURING,
    )


@given(parsers.parse("Csp Subarray {subarray_id} completes Configure"))
def csp_subarray_configure_complete(event_recorder, simulator_factory):
    csp_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.MID_CSP_DEVICE
    )
    event_recorder.subscribe_event(csp_sim, "obsState")
    assert event_recorder.has_change_event_occurred(
        csp_sim,
        "obsState",
        ObsState.READY,
    )


@given(
    parsers.parse(
        "Sdp Subarray {subarray_id} raises exception and goes back to "
        + "obsState IDLE"
    )
)
def sdp_subarray_returns_to_obsstate_idle(
    event_recorder, simulator_factory, command_input_factory
):
    sdp_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.MID_SDP_DEVICE
    )
    event_recorder.subscribe_event(sdp_sim, "obsState")
    valid_receiptor_json = prepare_json_args_for_commands(
        "science_A_receiver_address", command_input_factory
    )
    assert event_recorder.has_change_event_occurred(
        sdp_sim,
        "obsState",
        ObsState.IDLE,
    )
    sdp_sim.SetDirectreceiveAddresses(valid_receiptor_json)


@given(
    parsers.parse("the TMC SubarrayNode {subarray_id} stucks in CONFIGURING")
)
def given_tmc_subarray_stuck_configuring(
    subarray_node,
    event_recorder,
):
    event_recorder.subscribe_event(subarray_node.subarray_node, "obsState")
    event_recorder.subscribe_event(
        subarray_node.subarray_node, "longRunningCommandResult"
    )
    assert subarray_node.subarray_node.obsState == ObsState.CONFIGURING
    assert event_recorder.has_change_event_occurred(
        subarray_node.subarray_node,
        "longRunningCommandResult",
        (
            pytest.command_result[1][0],
            str(ResultCode.FAILED.value),
        ),
    )


@when(parsers.parse("I issue the command End on CSP Subarray {subarray_id}"))
def send_command(simulator_factory):
    csp_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.MID_CSP_DEVICE
    )
    csp_sim.End()


@then(
    parsers.parse(
        "the CSP subarray {subarray_id} transitions to obsState IDLE"
    )
)
def csp_subarray_transitions_to_idle(simulator_factory, event_recorder):
    csp_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.MID_CSP_DEVICE
    )
    event_recorder.subscribe_event(csp_sim, "obsState")
    assert event_recorder.has_change_event_occurred(
        csp_sim,
        "obsState",
        ObsState.IDLE,
    )


@then(
    parsers.parse(
        "Tmc SubarrayNode {subarray_id} transitions to obsState IDLE"
    )
)
def tmc_subarray_transitions_to_idle(subarray_node, event_recorder):
    event_recorder.subscribe_event(subarray_node.subarray_node, "obsState")
    assert event_recorder.has_change_event_occurred(
        subarray_node.subarray_node,
        "obsState",
        ObsState.IDLE,
    )
