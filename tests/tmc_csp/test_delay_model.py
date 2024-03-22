"""Test module to test delay functionality."""
import json

import pytest
from pytest_bdd import given, scenario, then, when
from ska_control_model import ObsState
from tango import DevState

from tests.resources.test_harness.central_node_mid import CentralNodeWrapperMid
from tests.resources.test_harness.event_recorder import EventRecorder
from tests.resources.test_harness.helpers import (
    calculate_epoch_difference,
    generate_ska_epoch_tai_value,
    prepare_json_args_for_centralnode_commands,
    prepare_json_args_for_commands,
    wait_for_delay_updates_stop_on_delay_model,
    wait_till_delay_values_are_populated,
)
from tests.resources.test_harness.subarray_node import SubarrayNodeWrapper
from tests.resources.test_harness.utils.common_utils import JsonFactory


@pytest.mark.tmc_csp
@scenario(
    "../features/tmc_csp/test_delay_model.feature",
    "TMC generates delay values",
)
def test_tmc_csp_configure_functionality() -> None:
    """
    Test case to verify delay generates properly.
    """


@given("the telescope is in ON state")
def check_telescope_is_in_on_state(
    central_node_mid: CentralNodeWrapperMid, event_recorder: EventRecorder
) -> None:
    """Ensure telescope is in ON state."""
    central_node_mid.move_to_on()
    event_recorder.subscribe_event(
        central_node_mid.central_node, "telescopeState"
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.central_node,
        "telescopeState",
        DevState.ON,
    )


@given("TMC subarray is in obsState IDLE")
def move_subarray_node_to_idle_obsstate(
    central_node_mid: CentralNodeWrapperMid,
    event_recorder: EventRecorder,
    command_input_factory: JsonFactory,
    subarray_id: str,
) -> None:
    """Move TMC Subarray to IDLE obsstate."""
    central_node_mid.set_subarray_id(subarray_id)
    assign_input_json = prepare_json_args_for_centralnode_commands(
        "assign_resources_mid", command_input_factory
    )
    # Create json for AssignResources commands with requested subarray_id
    assign_input = json.loads(assign_input_json)
    assign_input["subarray_id"] = int(subarray_id)
    central_node_mid.store_resources(json.dumps(assign_input))

    event_recorder.subscribe_event(central_node_mid.subarray_node, "obsState")
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.IDLE,
    )


@when("I configure the TMC subarray")
def invoke_configure_command(
    subarray_node: SubarrayNodeWrapper, command_input_factory: JsonFactory
) -> None:
    """Invoke Configure command."""
    configure_input_json = prepare_json_args_for_commands(
        "configure_mid", command_input_factory
    )
    subarray_node.store_configuration_data(configure_input_json)


@then(
    "CSP Subarray Leaf Node starts generating delay values with proper epoch"
)
def check_if_delay_values_are_generating(
    subarray_node: SubarrayNodeWrapper,
) -> None:
    """Check if delay values are generating."""
    ska_epoch_tai = generate_ska_epoch_tai_value
    delay_json, delay_generated_time = wait_till_delay_values_are_populated(
        subarray_node.csp_subarray_leaf_node
    )
    epoch_difference = calculate_epoch_difference(
        delay_generated_time, ska_epoch_tai, delay_json
    )
    assert epoch_difference < 30


@when("I end the observation")
def invoke_end_command(subarray_node: SubarrayNodeWrapper) -> None:
    """Invoke End command."""
    subarray_node.end_observation()


@then("CSP Subarray Leaf Node stops generating delay values")
def check_if_delay_values_are_stop_generating(
    subarray_node: SubarrayNodeWrapper,
) -> None:
    """Check if delay values are stop generating."""
    wait_for_delay_updates_stop_on_delay_model(
        subarray_node.csp_subarray_leaf_node
    )
