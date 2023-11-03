import json
import time

import pytest
from pytest_bdd import given, parsers, scenario, then, when
from ska_control_model import ObsState
from tango import DevState

from tests.conftest import LOGGER
from tests.resources.test_harness.constant import (
    COMMAND_FAILED_WITH_EXCEPTION_OBSSTATE_IDLE,
)
from tests.resources.test_harness.helpers import (
    get_device_simulators,
    prepare_json_args_for_centralnode_commands,
)


@pytest.mark.t1
@pytest.mark.bdd_assign
@pytest.mark.SKA_mid
@scenario(
    "../features/incremental_assign_resources_csp_subarray_failure.feature",
    "TMC behavior when CSP Subarray"
    " incremental AssignResources raises exception",
)
def test_incremental_assign_resources_csp_subarray_failure(
    central_node_mid, subarray_node, event_recorder, simulator_factory
):
    """
    Test to verify TMC failure handling when incremental AssignResources
    command fails on CSP Subarray. First AssignResources completes
    on CSP and SDP Subarray, and it transitions to obsState IDLE.
    Whereas after next AssignResources CSP Subarray raises exception and
    transitions again to obsState IDLE. As a handling ReleaseAllResources
    is invoked on SDP Subarray. SDP Subarray then moves to obsState
    EMPTY. SubarrayNode aggregates obsStates of the lower Subarrays
    and transitions to obsState EMPTY.
    Glossary:
    - "central_node_mid": fixture for a TMC CentralNode Mid under test
    which provides simulated master devices
    - "event_recorder": fixture for a MockTangoEventCallbackGroup
    for validating the subscribing and receiving events.
    - "simulator_factory": fixture for creating simulator devices for
    mid-Telescope respectively.
    """


@given("a TMC")
def given_tmc(central_node_mid, event_recorder):
    event_recorder.subscribe_event(
        central_node_mid.central_node, "telescopeState"
    )
    event_recorder.subscribe_event(central_node_mid.subarray_node, "obsState")
    LOGGER.info("Starting up the Telescope")
    central_node_mid.move_to_on()
    assert event_recorder.has_change_event_occurred(
        central_node_mid.central_node,
        "telescopeState",
        DevState.ON,
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.EMPTY,
    )


@given(
    parsers.parse(
        "AssignResources is executed"
        " successfully on SubarrayNode {subarray_id}"
    )
)
def given_assign_resources_executed_on_tmc_subarray(
    central_node_mid, event_recorder, simulator_factory, command_input_factory
):

    csp_sim, sdp_sim, _, _ = get_device_simulators(simulator_factory)
    event_recorder.subscribe_event(csp_sim, "obsState")
    event_recorder.subscribe_event(sdp_sim, "obsState")
    event_recorder.subscribe_event(central_node_mid.subarray_node, "obsState")

    assign_input_json = prepare_json_args_for_centralnode_commands(
        "incremental_assign_resources_01", command_input_factory
    )

    central_node_mid.perform_action("AssignResources", assign_input_json)
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.IDLE,
    )
    # wait before next AssignResources
    time.sleep(0.5)


@given(
    parsers.parse(
        "the next TMC SubarrayNode "
        "{subarray_id} assign resources is in progress"
    )
)
def given_tmc_subarray_incremental_assign_resources_is_in_progress(
    central_node_mid, event_recorder, simulator_factory, command_input_factory
):
    csp_sim, sdp_sim, _, _ = get_device_simulators(simulator_factory)
    event_recorder.subscribe_event(csp_sim, "obsState")
    event_recorder.subscribe_event(sdp_sim, "obsState")
    event_recorder.subscribe_event(central_node_mid.subarray_node, "obsState")

    assign_input_json = prepare_json_args_for_centralnode_commands(
        "incremental_assign_resources_02", command_input_factory
    )

    # After AssignResources invocation, CSP Subarray first transitions to
    # obsState RESOURCING and then again to the obsState IDLE due to fault
    # induction
    csp_sim.SetDefective(
        json.dumps(COMMAND_FAILED_WITH_EXCEPTION_OBSSTATE_IDLE)
    )
    central_node_mid.perform_action("AssignResources", assign_input_json)
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.RESOURCING,
    )


@given(parsers.parse("Sdp Subarray {subarray_id} returns to obsState IDLE"))
def sdp_subarray_assign_resources_complete(event_recorder, simulator_factory):
    _, sdp_sim, _, _ = get_device_simulators(simulator_factory)
    event_recorder.subscribe_event(sdp_sim, "obsState")
    assert event_recorder.has_change_event_occurred(
        sdp_sim,
        "obsState",
        ObsState.IDLE,
    )


@given(parsers.parse("Csp Subarray {subarray_id} completes assignResources"))
def csp_subarray_assign_resources_complete(event_recorder, simulator_factory):
    csp_sim, _, _, _ = get_device_simulators(simulator_factory)
    event_recorder.subscribe_event(csp_sim, "obsState")
    assert event_recorder.has_change_event_occurred(
        csp_sim,
        "obsState",
        ObsState.IDLE,
    )


@when(
    parsers.parse(
        "I issue the command ReleaseAllResources on SDP Subarray {subarray_id}"
    )
)
def send_command_release(simulator_factory):
    csp_sim, sdp_sim, _, _ = get_device_simulators(simulator_factory)
    sdp_sim.ReleaseAllResources()
    # Disable CSP Subarray fault
    csp_sim.SetDefective(json.dumps({"enabled": False}))


@then(
    parsers.parse(
        "the SDP subarray {subarray_id} transitions to obsState EMPTY"
    )
)
def sdp_subarray_transitions_to_empty(simulator_factory, event_recorder):
    _, sdp_sim, _, _ = get_device_simulators(simulator_factory)
    event_recorder.subscribe_event(sdp_sim, "obsState")
    assert event_recorder.has_change_event_occurred(
        sdp_sim,
        "obsState",
        ObsState.EMPTY,
    )


@then(
    parsers.parse(
        "Tmc SubarrayNode {subarray_id} transitions to obsState EMPTY"
    )
)
def tmc_subarray_transitions_to_empty(central_node_mid, event_recorder):
    event_recorder.subscribe_event(central_node_mid.subarray_node, "obsState")
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.EMPTY,
    )
