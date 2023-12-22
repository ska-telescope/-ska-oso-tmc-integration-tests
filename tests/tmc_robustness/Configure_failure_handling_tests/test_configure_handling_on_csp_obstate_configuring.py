import json

import pytest
from pytest_bdd import given, parsers, scenario, then, when
from ska_control_model import ObsState
from tango import DevState

from tests.resources.test_harness.constant import (
    OBS_STATE_CONFIGURING_STUCK_DEFECT,
)
from tests.resources.test_harness.helpers import (
    get_device_simulators,
    prepare_json_args_for_centralnode_commands,
    prepare_json_args_for_commands,
)
from tests.resources.test_harness.utils.enums import SimulatorDeviceType


@pytest.mark.skip(
    reason="Test passes independently, fails when executed with all tests"
)
@pytest.mark.bdd_configure
@pytest.mark.SKA_mid
@scenario(
    "../features/xtp-28834.feature",
    "TMC behavior when Csp Subarray is stuck in obsState CONFIGURING",
)
def test_configure_handling_on_csp_subarray_obsstate_configuring_failure():
    """
    Test to verify TMC failure handling when Configure command fails on
    CSP Subarray. Configure completes on SDP Subarray and
    it transtions to obsState IDLE.
    Whereas CSP Subarray is stuck in obsState CONFIGURING.
    As a handling Abort + Restart command sequence is executed on
    the Subarray to take it to the initial obsState EMPTY.
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
def given_tmc_subarray_assigns_resources(
    central_node_mid,
    subarray_node,
    event_recorder,
    simulator_factory,
    command_input_factory,
):
    csp_sim, sdp_sim, _, _ = get_device_simulators(simulator_factory)
    event_recorder.subscribe_event(csp_sim, "obsState")
    event_recorder.subscribe_event(sdp_sim, "obsState")
    assign_input_json = prepare_json_args_for_centralnode_commands(
        "assign_resources_mid", command_input_factory
    )
    central_node_mid.perform_action("AssignResources", assign_input_json)
    assert event_recorder.has_change_event_occurred(
        subarray_node.subarray_node,
        "obsState",
        ObsState.IDLE,
    )


@given(
    parsers.parse(
        "the TMC SubarrayNode {subarray_id} Configure is in progress"
    )
)
def given_tmc_subarray_configure_is_in_progress(
    subarray_node, event_recorder, simulator_factory, command_input_factory
):
    csp_sim, _, _, _ = get_device_simulators(simulator_factory)
    configure_input_json = prepare_json_args_for_commands(
        "configure_mid", command_input_factory
    )
    # Induce fault on CSP Subarray so that it is stuck in obsState CONFIGURING
    csp_sim.SetDefective(json.dumps(OBS_STATE_CONFIGURING_STUCK_DEFECT))
    subarray_node.execute_transition("Configure", configure_input_json)
    assert event_recorder.has_change_event_occurred(
        subarray_node.subarray_node,
        "obsState",
        ObsState.CONFIGURING,
    )


@given(parsers.parse("Sdp Subarray {subarray_id} completes Configure"))
def sdp_subarray_configure_complete(event_recorder, simulator_factory):
    sdp_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.MID_SDP_DEVICE
    )
    assert event_recorder.has_change_event_occurred(
        sdp_sim,
        "obsState",
        ObsState.READY,
    )


@given(
    parsers.parse(
        "Csp Subarray {subarray_id} is stuck in obsState CONFIGURING"
    )
)
def csp_subarray_stuck_in_configuring(event_recorder, simulator_factory):
    csp_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.MID_CSP_DEVICE
    )
    assert event_recorder.has_change_event_occurred(
        csp_sim,
        "obsState",
        ObsState.CONFIGURING,
    )
    # Disable CSP Subarray fault
    csp_sim.SetDefective(json.dumps({"enabled": False}))


@given(
    parsers.parse("the TMC SubarrayNode {subarray_id} stucks in CONFIGURING")
)
def given_tmc_subarray_stuck_configuring(
    subarray_node,
):
    assert subarray_node.subarray_node.obsState == ObsState.CONFIGURING


@when(
    parsers.parse(
        "I issue the Abort command on TMC SubarrayNode {subarray_id}"
    )
)
def send_command_abort(subarray_node, event_recorder):
    subarray_node.execute_transition("Abort", argin=None)
    assert event_recorder.has_change_event_occurred(
        subarray_node.subarray_node,
        "obsState",
        ObsState.ABORTING,
    )


@then(
    parsers.parse(
        "the SDP subarray {subarray_id} transitions to obsState ABORTED"
    )
)
def sdp_subarray_transitions_to_aborted(simulator_factory, event_recorder):
    sdp_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.MID_SDP_DEVICE
    )
    assert event_recorder.has_change_event_occurred(
        sdp_sim,
        "obsState",
        ObsState.ABORTED,
    )


@then(
    parsers.parse(
        "the CSP subarray {subarray_id} transitions to obsState ABORTED"
    )
)
def csp_subarray_transitions_to_aborted(simulator_factory, event_recorder):
    csp_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.MID_CSP_DEVICE
    )
    assert event_recorder.has_change_event_occurred(
        csp_sim,
        "obsState",
        ObsState.ABORTED,
    )


@then(
    parsers.parse(
        "Tmc SubarrayNode {subarray_id} transitions to obsState ABORTED"
    )
)
def tmc_subarray_transitions_to_aborted(subarray_node, event_recorder):
    assert event_recorder.has_change_event_occurred(
        subarray_node.subarray_node,
        "obsState",
        ObsState.ABORTED,
        lookahead=9,
    )


@when(
    parsers.parse(
        "I issue the Restart command on TMC SubarrayNode {subarray_id}"
    )
)
def send_command_restart(subarray_node, event_recorder):
    subarray_node.execute_transition("Restart", argin=None)
    assert event_recorder.has_change_event_occurred(
        subarray_node.subarray_node,
        "obsState",
        ObsState.RESTARTING,
    )


@then(
    parsers.parse(
        "the SDP subarray {subarray_id} transitions to obsState EMPTY"
    )
)
def sdp_subarray_transitions_to_empty(simulator_factory, event_recorder):
    sdp_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.MID_SDP_DEVICE
    )
    assert event_recorder.has_change_event_occurred(
        sdp_sim,
        "obsState",
        ObsState.EMPTY,
    )


@then(
    parsers.parse(
        "the CSP subarray {subarray_id} transitions to obsState EMPTY"
    )
)
def csp_subarray_transitions_to_empty(simulator_factory, event_recorder):
    csp_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.MID_CSP_DEVICE
    )
    assert event_recorder.has_change_event_occurred(
        csp_sim,
        "obsState",
        ObsState.EMPTY,
    )


@then(
    parsers.parse(
        "Tmc SubarrayNode {subarray_id} transitions to obsState EMPTY"
    )
)
def tmc_subarray_transitions_to_empty(subarray_node, event_recorder):
    assert event_recorder.has_change_event_occurred(
        subarray_node.subarray_node,
        "obsState",
        ObsState.EMPTY,
    )


@then(
    parsers.parse(
        "Configure command is executed successfully on the "
        + "Subarray {subarray_id}"
    )
)
def configure_executed_on_subarray(subarray_node, event_recorder):
    subarray_node.force_change_of_obs_state("READY")

    assert event_recorder.has_change_event_occurred(
        subarray_node.subarray_node,
        "obsState",
        ObsState.READY,
    )