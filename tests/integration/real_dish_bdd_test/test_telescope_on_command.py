"""BDD test Telescope On Command on DISH LMC"""

import pytest
from pytest_bdd import given, scenario, then, when
from tango import DevState

from tests.resources.test_harness.utils.enums import SimulatorDeviceType
from tests.resources.test_support.enum import DishMode


@pytest.mark.t1
@pytest.mark.real_dish
@scenario(
    "../features/check_on_command_on_real_dish.feature",
    "StartUp Telescope with TMC and DISH devices",
)
def test_telescope_on():
    """This test validates that TMC is able to invoke
    telesopeOn command on Dishlmc"""


@given(
    "a Telescope consisting of  TMC, DISH , simulated CSP and simulated SDP"
)
def given_tmc(central_node_mid, simulator_factory, event_recorder):
    """Given TMC"""
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


@when("I start up the telescope")
def turn_on_telescope(central_node_mid):
    """Invoke telescopeOn on TMC"""
    # Invoke TelescopeOn command
    central_node_mid.move_to_on()


@then("DISH must go to STANDBY-FP mode")
def check_dish_state(central_node_mid, event_recorder):
    """Checking Dish state after invoking
    telescopeOn command on central node"""
    event_recorder.subscribe_event(
        central_node_mid.dish_master_list[0], "dishMode"
    )
    event_recorder.subscribe_event(
        central_node_mid.dish_master_list[1], "dishMode"
    )
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


@then("telescope state is ON")
def check_telescope_state(central_node_mid, event_recorder):
    """Checking if TMC central node is ON"""
    event_recorder.subscribe_event(
        central_node_mid.central_node, "telescopeState"
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.central_node,
        "telescopeState",
        DevState.ON,
    )
