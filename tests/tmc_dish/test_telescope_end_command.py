"""Test module for TMC-DISH End functionality"""

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


@pytest.mark.t1
@pytest.mark.real_dish
@scenario(
    "../features/tmc_dish/check_end_command_on_real_dish.feature",
    "TMC executes End command on DISH.LMC",
)
def test_tmc_dish_end_telescope():
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

    Args:
        simulator_factory: fixture for SimulatorFactory class,
        which provides simulated master devices
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
        central_node_mid.central_node, "telescopeState"
    )
    central_node_mid.move_to_on()

    assert event_recorder.has_change_event_occurred(
        central_node_mid.central_node,
        "telescopeState",
        DevState.ON,
    )


@given(parsers.parse("TMC subarray {subarray_id} is in READY ObsState"))
def check_subarray_obstate(
    subarray_node, command_input_factory, event_recorder, central_node_mid
):
    """Method to check subarray is in READY obstate"""
    event_recorder.subscribe_event(central_node_mid.subarray_node, "obsState")
    assign_input_json = prepare_json_args_for_centralnode_commands(
        "assign_resources_mid", command_input_factory
    )
    central_node_mid.store_resources(assign_input_json)

    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.IDLE,
    )
    configure_input_json = prepare_json_args_for_commands(
        "configure_mid", command_input_factory
    )

    subarray_node.execute_transition("Configure", configure_input_json)
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.READY,
    )


@when(
    parsers.parse("I issued the End command to the TMC subarray {subarray_id}")
)
def invoke_configure(subarray_node):

    subarray_node.execute_transition("End")


@then("Dish Mode is transitioned to STANDBY-FP")
def check_dish_mode(central_node_mid, event_recorder):
    event_recorder.subscribe_event(
        central_node_mid.dish_master_list[0], "dishMode"
    )
    event_recorder.subscribe_event(
        central_node_mid.dish_master_list[1], "dishMode"
    )
    # event_recorder.subscribe_event(
    #     central_node_mid.dish_master_list[2], "dishMode"
    # )
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
    # assert event_recorder.has_change_event_occurred(
    #     central_node_mid.dish_master_list[2],
    #     "dishMode",
    #     DishMode.STANDBY_FP,
    # )


@then("Pointing State is transitioned to READY")
def check_dish_pointing_state(central_node_mid, event_recorder):
    event_recorder.subscribe_event(
        central_node_mid.dish_master_list[0], "pointingState"
    )
    event_recorder.subscribe_event(
        central_node_mid.dish_master_list[1], "pointingState"
    )
    # event_recorder.subscribe_event(
    #     central_node_mid.dish_master_list[2], "pointingState"
    # )
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
    # assert event_recorder.has_change_event_occurred(
    #     central_node_mid.dish_master_list[2],
    #     "pointingState",
    #     PointingState.READY,
    # )


@then(parsers.parse("TMC subarray {subarray_id} obsState transitions to IDLE"))
def check_subarray_obsState_ready(central_node_mid, event_recorder):
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.IDLE,
    )
