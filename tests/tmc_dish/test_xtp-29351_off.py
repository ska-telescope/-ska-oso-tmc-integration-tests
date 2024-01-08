"""Test module for TMC-DISH Off functionality"""

import pytest
from pytest_bdd import given, scenario, then, when
from tango import DevState

from tests.resources.test_harness.utils.enums import SimulatorDeviceType
from tests.resources.test_support.enum import DishMode


@pytest.mark.tmc_dish
@scenario(
    "../features/tmc_dish/xtp-29351_off.feature",
    "Shut down with TMC and DISH devices",
)
def test_tmc_dish_shutdown_telescope():
    """
    Test case to verify TMC-DISH ShutDown functionality
    Glossary:
        - "central_node_mid": fixture for a TMC CentralNode under test
        - "simulator_factory": fixture for SimulatorFactory class,
        which provides simulated master devices
        - "event_recorder": fixture for EventRecorder class
    """


@given(
    "a Telescope consisting of TMC, DISH, simulated CSP"
    " and simulated SDP is in ON state"
)
def check_tmc_and_dish_is_on(
    central_node_mid, event_recorder, simulator_factory
):
    """
    Given a TMC , DISH , simulated CSP and simulated in ON state
    """

    csp_master_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.MID_CSP_MASTER_DEVICE
    )
    sdp_master_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.MID_SDP_MASTER_DEVICE
    )

    event_recorder.subscribe_event(
        central_node_mid.central_node, "telescopeState"
    )
    event_recorder.subscribe_event(csp_master_sim, "State")
    event_recorder.subscribe_event(sdp_master_sim, "State")
    event_recorder.subscribe_event(
        central_node_mid.dish_master_list[0], "dishMode"
    )
    event_recorder.subscribe_event(
        central_node_mid.dish_master_list[1], "dishMode"
    )
    event_recorder.subscribe_event(
        central_node_mid.dish_master_list[2], "dishMode"
    )

    assert csp_master_sim.ping() > 0
    assert sdp_master_sim.ping() > 0
    assert central_node_mid.dish_master_list[0].ping() > 0
    assert central_node_mid.dish_master_list[1].ping() > 0
    assert central_node_mid.dish_master_list[2].ping() > 0
    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_master_list[0], "dishMode", DishMode.STANDBY_LP
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_master_list[1], "dishMode", DishMode.STANDBY_LP
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_master_list[2], "dishMode", DishMode.STANDBY_LP
    )

    central_node_mid.move_to_on()

    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_master_list[0], "dishMode", DishMode.STANDBY_FP
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_master_list[1], "dishMode", DishMode.STANDBY_FP
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_master_list[2], "dishMode", DishMode.STANDBY_FP
    )
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


@when("I switch off the telescope")
def turn_off_telescope(central_node_mid):
    """Invoke telescopeOff on TMC"""
    central_node_mid.move_to_off()


@then("DISH must go to STANDBY-LP mode")
def check_dish_state(central_node_mid, event_recorder):
    """Checking dishMode"""
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
