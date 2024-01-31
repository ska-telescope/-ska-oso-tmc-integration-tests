"""Test module for TMC-DISH End functionality"""

import time

import pytest
from pytest_bdd import given, parsers, scenario, then, when
from ska_tango_base.control_model import ObsState
from tango import DevState

from tests.resources.test_harness.helpers import (
    prepare_json_args_for_centralnode_commands,
    prepare_json_args_for_commands,
)
from tests.resources.test_harness.utils.enums import SimulatorDeviceType
from tests.resources.test_support.enum import DishMode, PointingState

@pytest.mark.skip(reason="This test will be fixed as part of sah-1476")
@pytest.mark.tmc_dish
@scenario(
    "../features/tmc_dish/xtp-29417_end.feature",
    "TMC executes End command on DISH.LMC",
)
def test_tmc_dish_end():
    """
    Test case to verify TMC-DISH End functionality

    Glossary:
        - "central_node_mid": fixture for a TMC CentralNode under test
        - "simulator_factory": fixture for SimulatorFactory class,
        which provides simulated master devices
        - "event_recorder": fixture for EventRecorder class
    """


@given("a Telescope consisting of TMC, DISH , simulated CSP and simulated SDP")
def given_tmc(central_node_mid, simulator_factory, event_recorder):
    """
    Given a TMC
    """
    csp_master_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.MID_CSP_MASTER_DEVICE
    )
    sdp_master_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.MID_SDP_MASTER_DEVICE
    )
    event_recorder.subscribe_event(csp_master_sim, "State")
    event_recorder.subscribe_event(sdp_master_sim, "State")

    assert csp_master_sim.ping() > 0
    assert sdp_master_sim.ping() > 0
    assert central_node_mid.dish_master_list[0].ping() > 0
    assert central_node_mid.dish_master_list[1].ping() > 0
    assert central_node_mid.dish_master_list[2].ping() > 0


@given("the Telescope is in ON state")
def move_dish_to_on(central_node_mid, event_recorder):
    """A method to put DISH to ON"""

    event_recorder.subscribe_event(
        central_node_mid.dish_master_list[0], "dishMode"
    )
    event_recorder.subscribe_event(
        central_node_mid.dish_master_list[1], "dishMode"
    )
    event_recorder.subscribe_event(
        central_node_mid.dish_master_list[2], "dishMode"
    )

    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_master_list[0],
        "dishMode",
        DishMode.STANDBY_LP,
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_master_list[1],
        "dishMode",
        DishMode.STANDBY_LP,
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_master_list[2],
        "dishMode",
        DishMode.STANDBY_LP,
    )

    # Wait for the DishLeafNode to get StandbyLP event form DishMaster before
    # invoking TelescopeOn command
    time.sleep(1)

    event_recorder.subscribe_event(
        central_node_mid.central_node, "telescopeState"
    )

    assert event_recorder.has_change_event_occurred(
        central_node_mid.central_node,
        "telescopeState",
        DevState.OFF,
    )

    central_node_mid.move_to_on()

    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_master_list[0],
        "dishMode",
        DishMode.STANDBY_FP,
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_master_list[1],
        "dishMode",
        DishMode.STANDBY_FP,
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_master_list[2],
        "dishMode",
        DishMode.STANDBY_FP,
    )

    # Wait for the DishLeafNode to get StandbyFP event form DishMaster before
    # invoking TelescopeOn command
    time.sleep(1)

    assert event_recorder.has_change_event_occurred(
        central_node_mid.sdp_master,
        "State",
        DevState.ON,
    )

    assert event_recorder.has_change_event_occurred(
        central_node_mid.csp_master,
        "State",
        DevState.ON,
    )

    assert event_recorder.has_change_event_occurred(
        central_node_mid.central_node,
        "telescopeState",
        DevState.ON,
    )


@given(parsers.parse("TMC subarray {subarray_id} is in READY ObsState"))
def check_subarray_obstate(
    subarray_node,
    command_input_factory,
    event_recorder,
    central_node_mid,
    subarray_id,
):
    """Method to check subarray is in READY obstate"""
    event_recorder.subscribe_event(subarray_node.subarray_node, "obsState")

    assign_input_json = prepare_json_args_for_centralnode_commands(
        "assign_resources_mid", command_input_factory
    )
    central_node_mid.set_subarray_id(subarray_id)
    central_node_mid.store_resources(assign_input_json)

    assert event_recorder.has_change_event_occurred(
        subarray_node.subarray_node,
        "obsState",
        ObsState.IDLE,
    )
    configure_input_json = prepare_json_args_for_commands(
        "configure_mid", command_input_factory
    )

    subarray_node.execute_transition("Configure", configure_input_json)

    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_master_list[0],
        "dishMode",
        DishMode.OPERATE,
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_master_list[1],
        "dishMode",
        DishMode.OPERATE,
    )
    event_recorder.subscribe_event(
        central_node_mid.dish_master_list[0], "pointingState"
    )
    event_recorder.subscribe_event(
        central_node_mid.dish_master_list[1], "pointingState"
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_master_list[0],
        "pointingState",
        PointingState.TRACK,
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_master_list[1],
        "pointingState",
        PointingState.TRACK,
    )
    assert event_recorder.has_change_event_occurred(
        subarray_node.subarray_node,
        "obsState",
        ObsState.READY,
    )


@when(
    parsers.parse("I issue the End command to the TMC subarray {subarray_id}")
)
def invoke_end(central_node_mid, subarray_node, subarray_id):
    """A method to invoke End command"""
    central_node_mid.set_subarray_id(subarray_id)
    subarray_node.execute_transition("End")


@then("dishMode transitions to STANDBY-FP obsState")
def check_dish_mode(central_node_mid, event_recorder):
    """Method to check Dish is in STANDBY-FP Dish Mode"""

    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_master_list[0],
        "dishMode",
        DishMode.STANDBY_FP,
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_master_list[1],
        "dishMode",
        DishMode.STANDBY_FP,
    )


@then("pointingState transitions to READY")
def check_dish_pointing_state(central_node_mid, event_recorder):
    """Method to check Dish is in READY Pointing State"""
    event_recorder.subscribe_event(
        central_node_mid.dish_master_list[0], "pointingState"
    )
    event_recorder.subscribe_event(
        central_node_mid.dish_master_list[1], "pointingState"
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_master_list[0],
        "pointingState",
        PointingState.READY,
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_master_list[1],
        "pointingState",
        PointingState.READY,
    )


@then(
    parsers.parse(
        "TMC subarray {subarray_id} obsState transitions to IDLE obsState"
    )
)
def check_subarray_obsState_idle(
    central_node_mid, subarray_node, event_recorder, subarray_id
):
    """Method to check subarray is in IDLE obstate"""
    central_node_mid.set_subarray_id(subarray_id)
    assert event_recorder.has_change_event_occurred(
        subarray_node.subarray_node,
        "obsState",
        ObsState.IDLE,
    )
