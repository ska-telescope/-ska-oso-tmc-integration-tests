"""BDD test Telescope Off Command on DISH LMC"""

import pytest
from pytest_bdd import given, scenario, then, when
from tango import DevState

from tests.conftest import wait_for_dish_mode_change
from tests.resources.test_support.common_utils.common_helpers import Waiter
from tests.resources.test_support.enum import DishMode


@pytest.mark.t2
@pytest.mark.real_dish
@scenario(
    "../features/check_off_command_on_real_dish.feature",
    "ShutDown with TMC and DISH devices",
)
def test_telescopeOff_command():
    """This test validates that TMC is able to invoke
    telesopeOff command on Dishlmc"""


@given("a Telescope consisting of TMC and DISH that is in ON state")
def turn_on_telescope(central_node_mid):
    """Given TMC"""
    central_node_mid.move_to_on()


@given("simulated SDP and CSP in ON state")
def check_devices_turn_on(central_node_mid, event_recorder):
    """Checking if simulate devices are turned ON"""
    event_recorder.subscribe_event(
        central_node_mid.sdp_master, "telescopeState"
    )
    event_recorder.subscribe_event(
        central_node_mid.csp_master, "telescopeState"
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.sdp_master,
        "State",
        DevState.OFF,
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.csp_master,
        "State",
        DevState.OFF,
    )


@given("telescope state is ON")
def check_telescope_state(central_node_mid, event_recorder):
    """Invoke telescopeOn on TMC"""

    event_recorder.subscribe_event(
        central_node_mid.central_node, "telescopeState"
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.central_node,
        "telescopeState",
        DevState.ON,
    )


@when("I switch off the telescope")
def turn_off_telescope(central_node_mid):
    """Invoke telescopeOff on TMC"""
    central_node_mid.move_to_off()


@then("DISH must go to STANDBY-LP mode")
def check_dish_state(central_node_mid):
    """Checking Dish state"""
    for dish in central_node_mid.real_dish_master_list:
        # Waiting for DISH LMC to respond
        wait_for_dish_mode_change(DishMode.STANDBY_LP, dish.dish_master_1, 30)
        wait_for_dish_mode_change(DishMode.STANDBY_LP, dish.dish_master_2, 30)
        the_waiter = Waiter()
        the_waiter.wait(50)
        # Check the dishMode of DISH LMC i.e STANDBY-LP
        assert dish.dish_master_1.dishMode.value == DishMode.STANDBY_LP
        assert dish.dish_master_2.dishMode.value == DishMode.STANDBY_LP


@then("telescope is OFF")
def check_telescopeOff_state(central_node_with_dish, event_recorder):
    """Checking if telescope is turned OFF"""
    event_recorder.subscribe_event(
        central_node_with_dish.central_node, "telescopeState"
    )
    assert event_recorder.has_change_event_occurred(
        central_node_with_dish.central_node,
        "telescopeState",
        DevState.OFF,
    )
