import pytest
from pytest_bdd import given, parsers, scenario, then, when
from ska_control_model import ObsState

from tests.resources.test_support.common_utils.result_code import ResultCode

result, message = "", ""


@pytest.mark.SKA_low
@scenario(
    "../features/check_abort_command.feature",
    "TMC executes Abort Command in EMPTY obsState.",
)
def test_abort_command_not_allowed_empty():
    """BDD test scenario for verifying execution of the Abort
    command in EMPTY obsState in TMC."""


@given("a Subarray in EMPTY obsState")
def given_tmc(subarray_node_low, event_recorder):
    """Subarray in EMPTY obsState"""
    event_recorder.subscribe_event(subarray_node_low.subarray_node, "obsState")
    event_recorder.subscribe_event(
        subarray_node_low.csp_subarray_leaf_node, "obsState"
    )
    event_recorder.subscribe_event(
        subarray_node_low.sdp_subarray_leaf_node, "obsState"
    )
    event_recorder.subscribe_event(
        subarray_node_low.mccs_subarray_leaf_node, "obsState"
    )
    subarray_node_low.move_to_on()
    assert event_recorder.has_change_event_occurred(
        subarray_node_low.subarray_node,
        "obsState",
        ObsState.EMPTY,
    )

    assert event_recorder.has_change_event_occurred(
        subarray_node_low.csp_subarray_leaf_node,
        "obsState",
        ObsState.EMPTY,
    )
    assert event_recorder.has_change_event_occurred(
        subarray_node_low.sdp_subarray_leaf_node,
        "obsState",
        ObsState.EMPTY,
    )
    assert event_recorder.has_change_event_occurred(
        subarray_node_low.mccs_subarray_leaf_node,
        "obsState",
        ObsState.EMPTY,
    )


@when(parsers("I Abort it"))
def invoke_abort_command(
    subarray_node_low,
):
    """Send a Abort command to the subarray."""
    result_code, unique_id = subarray_node_low.execute_transition("Abort")
    assert result_code[0] == ResultCode.STARTED


@then("TMC should reject the Abort command with ResultCode.Rejected")
def invalid_command_rejection():
    assert (
        "Abort command is not allowed in current subarray obsState"
        in message[0]
    )
    assert result[0] == ResultCode.REJECTED


@then("TMC subarray remains in EMPTY obsstate")
def tmc_status(subarray_node_low, event_recorder):
    assert event_recorder.has_change_event_occurred(
        subarray_node_low.subarray_node,
        "obsState",
        ObsState.EMPTY,
    )
    assert event_recorder.has_change_event_occurred(
        subarray_node_low.csp_subarray_leaf_node,
        "obsState",
        ObsState.EMPTY,
    )
    assert event_recorder.has_change_event_occurred(
        subarray_node_low.sdp_subarray_leaf_node,
        "obsState",
        ObsState.EMPTY,
    )
    assert event_recorder.has_change_event_occurred(
        subarray_node_low.mccs_subarray_leaf_node,
        "obsState",
        ObsState.EMPTY,
    )
