import json

import pytest
from pytest_bdd import given, parsers, scenario, then, when
from ska_control_model import ObsState
from ska_tango_base.commands import ResultCode
from tango import DevState

from tests.resources.test_harness.constant import (
    COMMAND_FAILED_WITH_EXCEPTION_OBSSTATE_IDLE,
)
from tests.resources.test_harness.helpers import (
    get_device_simulators,
    prepare_json_args_for_centralnode_commands,
    prepare_json_args_for_commands,
)
from tests.resources.test_harness.utils.enums import SimulatorDeviceType

@pytest.mark.bdd_configure
@pytest.mark.SKA_mid
@scenario(
    "../features/configure_csp_sdp_subarray_failure_scenario.feature",
    "TMC behavior when CSP and SDP Subarray raises exception for "
    "Configure command",
)
def test_configure_handling_on_csp_sdp_subarray_obsstate_idle_failure():
    """
    Test to verify TMC failure handling when Configure
    command fails on both CSP and SDP Subarrays.
    CSP and SDP Subarrays raise exception and transitions
    to obsState IDLE. SubarrayNode aggregates obsStates of the lower Subarrays
    and transitions to obsState IDLE.
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
    _, unique_id = central_node_mid.perform_action(
        "AssignResources", assign_input_json
    )
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
        "the TMC SubarrayNode {subarray_id} configure is in progress"
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

    csp_sim.SetDefective(
        json.dumps(COMMAND_FAILED_WITH_EXCEPTION_OBSSTATE_IDLE)
    )

    configure_input_json = prepare_json_args_for_commands(
        "configure_with_invalid_scan_type", command_input_factory
    )
    subarray_node.execute_transition(
        "Configure", configure_input_json
    )
    assert event_recorder.has_change_event_occurred(
        subarray_node.subarray_node,
        "obsState",
        ObsState.CONFIGURING,
    )


@when(
    parsers.parse(
        "Csp Subarray {subarray_id} raises exception and goes back "
        + "to obsState IDLE"
    )
)
def csp_subarray_returns_to_obsstate_idle(event_recorder, simulator_factory):
    csp_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.MID_CSP_DEVICE
    )
    event_recorder.subscribe_event(csp_sim, "obsState")
    assert event_recorder.has_change_event_occurred(
        csp_sim,
        "obsState",
        ObsState.IDLE,
    )


@when(
    parsers.parse(
        "Sdp Subarray {subarray_id} raises exception and goes back "
        + "to obsState IDLE"
    )
)
def sdp_subarray_returns_to_obsstate_idle(event_recorder, simulator_factory):
    sdp_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.MID_SDP_DEVICE
    )
    event_recorder.subscribe_event(sdp_sim, "obsState")
    assert event_recorder.has_change_event_occurred(
        sdp_sim,
        "obsState",
        ObsState.IDLE,
    )


@then(
    parsers.parse(
        "Tmc SubarrayNode {subarray_id} aggregates and goes " + "back to IDLE"
    )
)
def tmc_subarray_transitions_to_idle(
    subarray_node, simulator_factory, event_recorder
):
    csp_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.MID_CSP_DEVICE
    )
    event_recorder.subscribe_event(subarray_node.subarray_node, "obsState")
    assert event_recorder.has_change_event_occurred(
        subarray_node.subarray_node,
        "obsState",
        ObsState.IDLE,
    )
    # Disable CSP Subarray fault
    csp_sim.SetDefective(json.dumps({"enabled": False}))


@then(
    parsers.parse(
        "Configure command is executed successfully on the "
        + "Subarray {subarray_id}"
    )
)
def configure_executed_on_subarray(
    subarray_node, event_recorder
):
    event_recorder.subscribe_event(subarray_node.subarray_node, "obsState")
    subarray_node.force_change_of_obs_state("READY")
    assert event_recorder.has_change_event_occurred(
        subarray_node.subarray_node,
        "obsState",
        ObsState.READY,
    )
