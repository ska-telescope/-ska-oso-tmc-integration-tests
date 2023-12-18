"""BDD test Telescope On Command on DISH LMC"""

import pytest
from pytest_bdd import given, scenario, then, when
from tango import DevState

from tests.conftest import wait_for_dish_mode_change
from tests.resources.test_support.common_utils.common_helpers import Waiter
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


# Given a Telescope consisting of  TMC, DISH , simulated CSP and simulated SDP
@given(
    "a Telescope consisting of  TMC, DISH , simulated CSP and simulated SDP"
)
def given_tmc():
    "Given TMC"


@given("telescope state is OFF")
def given_tmc_off(central_node_with_dish, event_recorder):
    """"""
    event_recorder.subscribe_event(
        central_node_with_dish.central_node, "telescopeState"
    )
    assert event_recorder.has_change_event_occurred(
        central_node_with_dish.central_node,
        "telescopeState",
        DevState.OFF,
    )


@when("I start up the telescope")
def turn_on_telescope(central_node_with_dish):
    """"""
    # Invoke TelescopeOn command
    central_node_with_dish.move_to_on()


@then("DISH must go to STANDBY-FP mode")
def check_dish_state(central_node_with_dish, event_recorder):

    event_recorder.subscribe_event(
        central_node_with_dish.central_node, "telescopeState"
    )
    # Waiting for DISH LMC to respond
    wait_for_dish_mode_change(
        DishMode.STANDBY_FP, central_node_with_dish.dish_master_1, 30
    )
    wait_for_dish_mode_change(
        DishMode.STANDBY_FP, central_node_with_dish.dish_master_2, 30
    )
    the_waiter = Waiter()
    the_waiter.wait(50)
    # Check the dishMode of DISH LMC i.e STANDBYFP
    assert (
        central_node_with_dish.dish_master_1.dishMode.value
        == DishMode.STANDBY_FP
    )
    assert (
        central_node_with_dish.dish_master_2.dishMode.value
        == DishMode.STANDBY_FP
    )


@then("telescope state is ON")
def check_telescope_state(central_node_with_dish, event_recorder):
    assert event_recorder.has_change_event_occurred(
        central_node_with_dish.central_node,
        "telescopeState",
        DevState.ON,
    )
