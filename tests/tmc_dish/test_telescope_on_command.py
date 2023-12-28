"""Test module for TMC-DISH StartUp functionality"""

import pytest
from pytest_bdd import given, scenario, then, when
from tango import DevState

from tests.resources.test_harness.utils.enums import SimulatorDeviceType
from tests.resources.test_support.enum import DishMode


@pytest.mark.real_dish
@scenario(
    "../features/check_on_command_on_real_dish.feature",
    "Start up Telescope with TMC and DISH devices",
)
def test_tmc_dish_startup_telescope():
    """
    Test case to verify TMC-DISH StartUp functionality

    Glossary:
        - "central_node_mid": fixture for a TMC CentralNode under test
        - "simulator_factory": fixture for SimulatorFactory class,
        which provides simulated master devices
        - "event_recorder": fixture for EventRecorder class
    """


@given(
    "a Telescope consisting of  TMC, DISH , simulated CSP and simulated SDP"
)
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


@when("I start up the telescope")
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
    event_recorder.subscribe_event(
        central_node_mid.central_node, "telescopeState"
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.central_node,
        "telescopeState",
        DevState.OFF,
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
    central_node_mid.move_to_on()


@then("DISH must go to STANDBY-FP mode")
def check_dish_is_on(central_node_mid, event_recorder):
    """Method to check dishMode after invoking
    telescopeOn command on central node"""
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


@then("telescope state is ON")
def check_telescope_state(central_node_mid, event_recorder):
    """Method to check if TMC central node is ON"""

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
