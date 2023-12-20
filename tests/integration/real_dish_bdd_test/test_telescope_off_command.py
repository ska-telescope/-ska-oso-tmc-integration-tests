"""BDD test Telescope Off Command on DISH LMC"""

import pytest
from pytest_bdd import given, scenario, then, when
from tango import DevState

from tests.resources.test_harness.utils.enums import SimulatorDeviceType
from tests.resources.test_support.enum import DishMode


@pytest.mark.t1
@pytest.mark.real_dish
@scenario(
    "../features/check_off_command_on_real_dish.feature",
    "ShutDown with TMC and DISH devices",
)
def test_telescopeOff_command():
    """This test validates that TMC is able to invoke
    telesopeOff command on Dishlmc"""


@given("a Telescope consisting of TMC and DISH that is in ON state")
def turn_on_telescope(central_node_mid, event_recorder):
    """Given TMC"""
    event_recorder.subscribe_event(
        central_node_mid.central_node, "telescopeState"
    )
    event_recorder.subscribe_event(
        central_node_mid.dish_master_list[0], "dishMode"
    )
    event_recorder.subscribe_event(
        central_node_mid.dish_master_list[1], "dishMode"
    )

    if central_node_mid.telescope_state != "ON":
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
        central_node_mid.central_node,
        "telescopeState",
        DevState.ON,
    )


@given("simulated SDP and CSP in ON state")
def check_devices_turn_on(event_recorder, simulator_factory):
    """Checking if simulate devices are turned ON"""
    csp_master_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.MID_CSP_MASTER_DEVICE
    )
    sdp_master_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.MID_SDP_MASTER_DEVICE
    )
    event_recorder.subscribe_event(csp_master_sim, "State")
    event_recorder.subscribe_event(sdp_master_sim, "State")

    assert event_recorder.has_change_event_occurred(
        csp_master_sim,
        "State",
        DevState.ON,
    )
    assert event_recorder.has_change_event_occurred(
        sdp_master_sim,
        "State",
        DevState.ON,
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
def check_dish_state(central_node_mid, event_recorder):
    """Checking dishMode"""
    event_recorder.subscribe_event(
        central_node_mid.dish_master_list[0], "dishMode"
    )
    event_recorder.subscribe_event(
        central_node_mid.dish_master_list[1], "dishMode"
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


@then("telescope is OFF")
def check_telescopeOff_state(central_node_mid, event_recorder):
    """Checking if telescope is turned OFF"""
    event_recorder.subscribe_event(
        central_node_mid.central_node, "telescopeState"
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.central_node,
        "telescopeState",
        DevState.OFF,
    )
