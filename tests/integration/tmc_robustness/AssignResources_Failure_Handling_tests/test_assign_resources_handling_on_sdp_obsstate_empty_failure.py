import pytest
from pytest_bdd import given, parsers, scenario, then, when
from ska_control_model import ObsState
from ska_tango_testing.mock.placeholders import Anything
from tango import DevState

from tests.conftest import LOGGER
from tests.resources.test_harness.helpers import (
    get_device_simulators,
    prepare_json_args_for_centralnode_commands,
)


@pytest.mark.bdd_assign
@pytest.mark.SKA_mid
@scenario(
    "../features/assign_resources_subsystem_failure_scenarios.feature",
    "TMC behavior when SDP Subarray AssignResources raises exception",
)
def test_assign_resources_handling_on_sdp_subarray_obsstate_empty_failure(
    central_node_mid, subarray_node, event_recorder, simulator_factory
):
    """
    Test to verify TMC failure handling when AssignResources
    command fails on SDP Subarray. AssignResources completes
    on CSP Subarray and it transtions to obsState IDLE.
    Whereas SDP Subarray raises exception and transitions
    to obsState EMPTY. As a handling ReleaseAllResources
    is invoked on CSP Subarray. CSP Subarray then moves to obsState
    EMPTY. SubarrayNode aggregates obsStates of the lower Subarrays
    and transitions to obsState EMPTY.
    Glossary:
    - "central_node_mid": fixture for a TMC CentralNode Mid under test
    which provides simulated master devices
    - "event_recorder": fixture for a MockTangoEventCallbackGroup
    for validating the subscribing and receiving events.
    - "simulator_factory": fixtur for creating simulator devices for
    mid Telescope respectively.
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
        "the TMC SubarrayNode {subarray_id} assign resources is in progress"
    )
)
def given_tmc_subarray_assign_resources_is_in_progress(
    central_node_mid, event_recorder, simulator_factory, command_input_factory
):
    csp_sim, sdp_sim, _, _ = get_device_simulators(simulator_factory)
    event_recorder.subscribe_event(csp_sim, "obsState")
    event_recorder.subscribe_event(sdp_sim, "obsState")
    event_recorder.subscribe_event(central_node_mid.subarray_node, "obsState")

    # Induce fault on SDP Subarry so that it raises exception and
    # returns to the obsState EMPTY
    assign_input_json = prepare_json_args_for_centralnode_commands(
        "assign_resources_mid_invalid_sdp_resources", command_input_factory
    )
    central_node_mid.perform_action("AssignResources", assign_input_json)
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.RESOURCING,
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


@given(parsers.parse("Sdp Subarray {subarray_id} returns to obsState EMPTY"))
def sdp_subarray_returns_to_obsstate_empty(event_recorder, simulator_factory):
    _, sdp_sim, _, _ = get_device_simulators(simulator_factory)
    event_recorder.subscribe_event(sdp_sim, "obsState")
    assert event_recorder.has_change_event_occurred(
        sdp_sim,
        "obsState",
        ObsState.EMPTY,
    )


@given(
    parsers.parse("the TMC SubarrayNode {subarray_id} stucks in RESOURCING")
)
def given_tmc_subarray_stuck_resourcing(
    central_node_mid,
    subarray_node,
    event_recorder,
):
    event_recorder.subscribe_event(central_node_mid.subarray_node, "obsState")
    event_recorder.subscribe_event(
        central_node_mid.subarray_node, "longRunningCommandResult"
    )
    LOGGER.info(
        "SubarrayNode ObsState is: %s", central_node_mid.subarray_node.obsState
    )
    assert central_node_mid.subarray_node.obsState == ObsState.RESOURCING
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "longRunningCommandResult",
        Anything,
    )


@when(
    parsers.parse(
        "I issue the command ReleaseAllResources on CSP Subarray {subarray_id}"
    )
)
def send_command(simulator_factory):
    csp_sim, sdp_sim, _, _ = get_device_simulators(simulator_factory)
    csp_sim.ReleaseAllResources()


@then(
    parsers.parse(
        "the CSP subarray {subarray_id} transitions to obsState EMPTY"
    )
)
def csp_subarray_transitions_to_empty(simulator_factory, event_recorder):
    csp_sim, _, _, _ = get_device_simulators(simulator_factory)
    event_recorder.subscribe_event(csp_sim, "obsState")
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
def tmc_subarray_transitions_to_empty(central_node_mid, event_recorder):
    event_recorder.subscribe_event(central_node_mid.subarray_node, "obsState")
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.EMPTY,
    )
