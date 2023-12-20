"""Test module for TMC-SDP ShutDown functionality"""
import pytest
from pytest_bdd import given, scenario, then, when
from tango import DevState

from tests.resources.test_harness.helpers import get_master_device_simulators
from tests.resources.test_harness.utils.enums import DishMode


@pytest.mark.real_sdp
@scenario(
    "../features/shut_down_tmc_sdp.feature",
    "Switch off the telescope having TMC and SDP subsystems",
)
def test_tmc_sdp_shutdown_telescope():
    """
    Test case to verify TMC-SDP ShutDown functionality
    Glossary:
        - "central_node_mid": fixture for a TMC CentralNode under test
        - "simulator_factory": fixture for SimulatorFactory class,
        which provides simulated subarray and master devices
        - "event_recorder": fixture for EventRecorder class
    """


@given("a Telescope consisting of TMC and SDP that is in ON State")
def check_tmc_and_sdp_is_on(central_node_mid, event_recorder):
    """
    Given a TMC and SDP in ON state
    """
    event_recorder.subscribe_event(
        central_node_mid.central_node, "telescopeState"
    )
    event_recorder.subscribe_event(central_node_mid.sdp_master, "State")
    event_recorder.subscribe_event(
        central_node_mid.subarray_devices["sdp_subarray"], "State"
    )

    if central_node_mid.telescope_state != "ON":
        central_node_mid.move_to_on()

    assert event_recorder.has_change_event_occurred(
        central_node_mid.sdp_master,
        "State",
        DevState.ON,
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_devices["sdp_subarray"],
        "State",
        DevState.ON,
    )


@given("simulated CSP and Dish in ON States")
def check_simulated_devices_states(simulator_factory, event_recorder):
    """A method to check CSP and Dish"""
    (
        csp_master_sim,
        _,
        dish_master_sim_1,
        dish_master_sim_2,
    ) = get_master_device_simulators(simulator_factory)

    event_recorder.subscribe_event(csp_master_sim, "State")
    event_recorder.subscribe_event(dish_master_sim_1, "dishMode")
    event_recorder.subscribe_event(dish_master_sim_2, "dishMode")

    assert event_recorder.has_change_event_occurred(
        csp_master_sim,
        "State",
        DevState.ON,
    )
    assert event_recorder.has_change_event_occurred(
        dish_master_sim_1,
        "dishMode",
        DishMode.STANDBY_FP,
    )
    assert event_recorder.has_change_event_occurred(
        dish_master_sim_2,
        "dishMode",
        DishMode.STANDBY_FP,
    )


@given("telescope state is ON")
def check_telescope_state_is_on(central_node_mid, event_recorder):
    """A method to check CentralNode.telescopeState"""
    assert event_recorder.has_change_event_occurred(
        central_node_mid.central_node,
        "telescopeState",
        DevState.ON,
    )


@when("I switch off the telescope")
def move_sdp_to_off(central_node_mid):
    """A method to put SDP to OFF"""
    central_node_mid.move_to_off()


@then("the sdp must go to OFF State")
def check_sdp_is_off(central_node_mid, event_recorder):
    """A method to check SDP State"""
    assert event_recorder.has_change_event_occurred(
        central_node_mid.sdp_master,
        "State",
        DevState.OFF,
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_devices["sdp_subarray"],
        "State",
        DevState.OFF,
    )


@then("telescope state is OFF")
def check_telescope_state_off(central_node_mid, event_recorder):
    """A method to check CentralNode.telescopeState"""
    assert event_recorder.has_change_event_occurred(
        central_node_mid.central_node,
        "telescopeState",
        DevState.OFF,
    )
    assert 0