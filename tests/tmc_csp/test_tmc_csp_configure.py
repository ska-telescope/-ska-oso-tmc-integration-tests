"""Test TMC-CSP COnfigure"""
import logging

import pytest
from ska_control_model import ObsState
from tango import DevState

from tests.resources.test_harness.helpers import (
    prepare_json_args_for_centralnode_commands,
    prepare_json_args_for_commands,
)

LOGGER = logging.getLogger(__name__)


@pytest.mark.real_csp_mid
def test_tmc_csp_configure(
    central_node_mid,
    event_recorder,
    command_input_factory,
):
    """Test TMC-CSP COnfigure"""
    central_node_mid.wait.set_wait_for_csp_master_to_become_off()
    central_node_mid.csp_master.adminMode = 0
    central_node_mid.wait.wait(500)
    csp_master_state = central_node_mid.csp_master.state()
    assert csp_master_state is DevState.OFF
    central_node_mid.move_to_on()
    event_recorder.subscribe_event(
        central_node_mid.central_node, "telescopeState"
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.central_node,
        "telescopeState",
        DevState.ON,
        lookahead=10,
    )

    assign_input_json = prepare_json_args_for_centralnode_commands(
        "assign_resources_mid", command_input_factory
    )
    central_node_mid.perform_action("AssignResources", assign_input_json)
    event_recorder.subscribe_event(central_node_mid.subarray_node, "obsState")
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.IDLE,
        lookahead=20,
    )

    san_obsstate = central_node_mid.subarray_node.obsState
    LOGGER.info("central_node_mid.subarray_node: %s", san_obsstate)

    configure_input_json = prepare_json_args_for_commands(
        "configure_mid", command_input_factory
    )
    central_node_mid.subarray_node.Configure(configure_input_json)
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.READY,
        lookahead=20,
    )
    san_obsstate = central_node_mid.subarray_node.obsState
    LOGGER.info("central_node_mid.subarray_node: %s", san_obsstate)

    central_node_mid.subarray_node.End()
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.IDLE,
        lookahead=20,
    )
    san_obsstate = central_node_mid.subarray_node.obsState
    LOGGER.info("central_node_mid.subarray_node: %s", san_obsstate)
