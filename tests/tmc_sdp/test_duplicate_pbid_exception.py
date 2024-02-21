"""TMC SubarrayNode handles the exception duplicate eb-id raised
by SDP subarray"""
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
from tests.resources.test_support.constant import (
    tmc_sdp_subarray_leaf_node,
    tmc_subarraynode1,
)


@pytest.mark.tmc_sdp
@pytest.mark.SKA_mid
@scenario(
    "../features/sdp_exception.feature",
    "TMC SubarrayNode handles the exception duplicate"
    " eb-id raised by SDP subarray",
)
def test_duplicate_ebid_exception_propogation(
    central_node_mid, subarray_node, event_recorder, simulator_factory
):
    """
    Test to verify TMC failure handling when duplicate EB ID is sent to
    SDP,command raises exception on SDP Subarray.
    After first AssignResources completes
    on SDP and CSP Subarrays, and it transitions to obsState IDLE.
    Whereas after next AssignResources SDP Subarray is  in obsState
    IDLE.Test makes sure that exception sent by SDP gets caught by TMC
    and gets propagated to central node and is available in long running
    attribute of central node. As a handling Abort + Restart command sequence
    is executed on
    the Subarray to take it to the initial obsState IDLE.
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
    """
    Perform initial set up and subscribe events
    """
    event_recorder.subscribe_event(
        central_node_mid.central_node, "telescopeState"
    )
    event_recorder.subscribe_event(central_node_mid.subarray_node, "obsState")
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
        "AssignResources is executed with {input_json1}"
        " successfully on SubarrayNode {subarray_id}"
    )
)
def given_assign_resources_executed_on_tmc_subarray(
    central_node_mid,
    event_recorder,
    input_json1,
    command_input_factory,
):
    """
    AssignResources is executed with input_json1 successfully
    on SubarrayNode 1.
    """

    event_recorder.subscribe_event(
        central_node_mid.central_node, "longRunningCommandResult"
    )
    assign_input_json = prepare_json_args_for_centralnode_commands(
        input_json1, command_input_factory
    )

    _, unique_id = central_node_mid.perform_action(
        "AssignResources", assign_input_json
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.IDLE,
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.central_node,
        "longRunningCommandResult",
        (unique_id[0], Anything),
    )


@given(
    parsers.parse(
        "TMC executes second AssignResources command with duplicate eb-id"
    )
)
def given_tmc_subarray_incremental_assign_resources_is_in_progress(
    central_node_mid,
    event_recorder,
    simulator_factory,
    input_json1,
    command_input_factory,
    shared_context,
):
    """
    TMC executes second AssignResources command with duplicate eb-id
    """
    event_recorder.subscribe_event(
        central_node_mid.central_node, "longRunningCommandResult"
    )
    assign_input_json = prepare_json_args_for_centralnode_commands(
        input_json1, command_input_factory
    )

    # Provide assign resources JSON with duplicate eb_id to get the
    # exception from SDP Subarray

    _, unique_id = central_node_mid.perform_action(
        "AssignResources", assign_input_json
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.RESOURCING,
    )
    shared_context.unique_id = unique_id

    csp_sim, _, _, _, _, _ = get_device_simulators(simulator_factory)
    event_recorder.subscribe_event(csp_sim, "obsState")
    assert event_recorder.has_change_event_occurred(
        csp_sim,
        "obsState",
        ObsState.IDLE,
    )

    LOGGER.info("CSP ObsState is ObsState.IDLE")


@then(
    parsers.parse(
        "SDP {subarray_id} throws exception and remain in IDLE status"
    )
)
def sdp_subarray_remains_in_idle(
    event_recorder, simulator_factory, central_node_mid
):
    """
    Check if SDP remains in IDLE status
    """
    _, sdp_sim, _, _, _, _ = get_device_simulators(simulator_factory)
    event_recorder.subscribe_event(sdp_sim, "obsState")
    assert event_recorder.has_change_event_occurred(
        sdp_sim,
        "obsState",
        ObsState.IDLE,
    )

    event_recorder.subscribe_event(
        central_node_mid.subarray_node, "longRunningCommandResult"
    )
    LOGGER.info(
        "SubarrayNode ObsState is %s", central_node_mid.subarray_node.obsState
    )
    assert central_node_mid.subarray_node.obsState == ObsState.RESOURCING


@then(parsers.parse("exception is propagated to central node"))
def check_exception_propagation_to_central_node(
    central_node_mid,
    event_recorder,
    shared_context,
):
    """
    Check exception propagation
    """
    exception_message = (
        f"Exception occurred on device: {tmc_subarraynode1}: "
        + "Exception occurred on the following devices:\n"
        + f"{tmc_sdp_subarray_leaf_node}: "
        + "Execution block eb-mvp01-20210623-00000 already exists\n"
    )

    event_recorder.has_change_event_occurred(
        central_node_mid.central_node,
        attribute_name="longRunningCommandResult",
        attribute_value=(shared_context.unique_id[0], exception_message),
    )


@then(
    parsers.parse(
        "I issue the Abort command on TMC SubarrayNode {subarray_id}"
    )
)
def send_command_abort(central_node_mid):
    """
    Issue Abort command
    """
    central_node_mid.subarray_node.Abort()


@then(
    parsers.parse(
        "the CSP, SDP and TMC subarray {subarray_id} transitions to "
        + "obsState ABORTED"
    )
)
def subarray_transitions_to_aborted(
    central_node_mid, simulator_factory, event_recorder
):
    """
    Check if TMC subarray , CSP Subarray and real SDP Subarray
    move to abort.
    """
    csp_sim, sdp_sim, _, _, _, _ = get_device_simulators(simulator_factory)
    event_recorder.subscribe_event(csp_sim, "obsState")
    assert event_recorder.has_change_event_occurred(
        csp_sim,
        "obsState",
        ObsState.ABORTED,
    )
    event_recorder.subscribe_event(sdp_sim, "obsState")
    assert event_recorder.has_change_event_occurred(
        sdp_sim,
        "obsState",
        ObsState.ABORTED,
    )

    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.ABORTED,
    )


@when(
    parsers.parse(
        "I issue the Restart command on TMC SubarrayNode {subarray_id}"
    )
)
def send_command_restart(central_node_mid):
    """
    Issue restart command.
    """
    central_node_mid.subarray_node.Restart()


@then(
    parsers.parse(
        "the CSP, SDP and TMC subarray {subarray_id} transitions to "
        + "obsState EMPTY"
    )
)
def subarray_transitions_to_empty(
    central_node_mid, simulator_factory, event_recorder
):
    """
    Check if CSP, SDP and TMC subarray  transitions to obsState EMPTY
    """
    csp_sim, sdp_sim, _, _, _, _ = get_device_simulators(simulator_factory)
    event_recorder.subscribe_event(csp_sim, "obsState")
    assert event_recorder.has_change_event_occurred(
        csp_sim,
        "obsState",
        ObsState.EMPTY,
    )
    event_recorder.subscribe_event(sdp_sim, "obsState")
    assert event_recorder.has_change_event_occurred(
        sdp_sim,
        "obsState",
        ObsState.EMPTY,
    )

    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.EMPTY,
    )


@then(
    parsers.parse(
        "AssignResources command is executed successfully on the "
        + "Subarray {subarray_id}"
    )
)
def assign_resources_executed_on_subarray(
    central_node_mid, event_recorder, command_input_factory
):
    """
    Check assignResources command is executed successfully
    """

    event_recorder.subscribe_event(
        central_node_mid.central_node, "longRunningCommandResult"
    )
    assign_input_json = prepare_json_args_for_centralnode_commands(
        "assign_resources_mid", command_input_factory
    )

    central_node_mid.store_resources(assign_input_json)

    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.IDLE,
    )
