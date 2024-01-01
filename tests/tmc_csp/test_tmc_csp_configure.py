"""Test module to test TMC-CSP Configure functionality."""
import json
import logging
import time

import pytest
from jsonschema import validate
from pytest_bdd import given, parsers, scenario, then, when
from ska_control_model import ObsState
from tango import DevState

from tests.resources.test_harness.central_node_mid import CentralNodeWrapperMid
from tests.resources.test_harness.event_recorder import EventRecorder
from tests.resources.test_harness.helpers import (
    prepare_json_args_for_centralnode_commands,
    prepare_json_args_for_commands,
    prepare_schema_for_attribute_or_command,
    wait_csp_master_off,
)
from tests.resources.test_harness.utils.common_utils import JsonFactory

LOGGER = logging.getLogger(__name__)
TIME_OUT = 15


@pytest.mark.tmc_csp
@scenario(
    "../features/tmc_csp/xtp_29345_configure.feature",
    "Configure a CSP subarray for a scan using TMC",
)
def test_tmc_csp_configure_functionality() -> None:
    """
    Test case to verify TMC-CSP Configure functionality
    """


@given("the telescope is in ON state")
def check_telescope_is_in_on_state(
    central_node_mid: CentralNodeWrapperMid, event_recorder: EventRecorder
) -> None:
    """Ensure telescope is in ON state."""
    if central_node_mid.csp_master.adminMode != 0:
        central_node_mid.csp_master.adminMode = 0
        wait_csp_master_off()
    central_node_mid.move_to_on()
    event_recorder.subscribe_event(
        central_node_mid.central_node, "telescopeState"
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.central_node,
        "telescopeState",
        DevState.ON,
        lookahead=15,
    )


@given(parsers.parse("TMC subarray {subarray_id} in ObsState IDLE"))
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
    central_node_mid.perform_action(
        "AssignResources", json.dumps(assign_input)
    )

    event_recorder.subscribe_event(central_node_mid.subarray_node, "obsState")
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.IDLE,
        lookahead=20,
    )


@when(
    parsers.parse(
        "I issue the Configure command to the TMC subarray {subarray_id}"
    )
)
def invoke_configure_command(
    central_node_mid: CentralNodeWrapperMid, command_input_factory: JsonFactory
) -> None:
    """Invoke Configure command."""
    configure_input_json = prepare_json_args_for_commands(
        "configure_mid", command_input_factory
    )
    central_node_mid.subarray_node.Configure(configure_input_json)


@then(
    parsers.parse(
        "the CSP subarray {subarray_id} transitions to ObsState READY"
    )
)
def check_if_csp_subarray_moved_to_ready_obsstate(
    central_node_mid: CentralNodeWrapperMid, event_recorder: EventRecorder
) -> None:
    """Ensure CSP subarray is moved to READY obsstate"""
    event_recorder.subscribe_event(
        central_node_mid.subarray_devices["csp_subarray"], "obsState"
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_devices["csp_subarray"],
        "obsState",
        ObsState.READY,
    )


@then(
    parsers.parse(
        "the TMC subarray {subarray_id} transitions to ObsState READY"
    )
)
def check_if_tmc_subarray_moved_to_ready_obsstate(
    central_node_mid: CentralNodeWrapperMid, event_recorder: EventRecorder
) -> None:
    """Ensure TMC Subarray is moved to READY obsstate"""
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.READY,
        lookahead=20,
    )


@then(
    parsers.parse(
        "CSP subarray leaf node {subarray_id} starts generating delay values"
    )
)
def check_if_delay_values_are_generating(
    central_node_mid: CentralNodeWrapperMid, command_input_factory: JsonFactory
) -> None:
    """Check id delay model is generating."""
    start_time = time.time()
    while central_node_mid.csp_subarray_leaf_node.delayModel == "no_value" or (
        time.time() - start_time < TIME_OUT
    ):
        time.sleep(1)

    delay_model_json = central_node_mid.csp_subarray_leaf_node.delayModel
    delay_model_schema = prepare_schema_for_attribute_or_command(
        "delay_model_schema", command_input_factory
    )

    try:
        # Validate delay model json
        validate(json.loads(delay_model_json), json.loads(delay_model_schema))
    except Exception as e:
        LOGGER.exception(e)
