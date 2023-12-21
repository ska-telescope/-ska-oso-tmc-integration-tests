"""Test module for TMC-CSP standby functionality"""
import logging
import time

import pytest
from pytest_bdd import given, scenario, then, when
from tango import DevState

from tests.resources.test_harness.helpers import get_master_device_simulators

LOGGER = logging.getLogger(__name__)


@pytest.mark.real_csp_mid
@scenario(
    "../features/tmc_csp_standby.feature",
    "Standby the Telescope with real TMC and CSP devices",
)
def test_tmc_csp_standby_telescope():
    """
    Test case to verify TMC-CSP Standby functionality
    """


@given(
    "a Telescope consisting of TMC, CSP, simulated DISH and simulated"
    + " SDP devices"
)
def check_a_tmc(central_node_mid, simulator_factory):
    """
    Given a TMC

    Args:
        simulator_factory: fixture for SimulatorFactory class,
        which provides simulated subarray and master devices
    """
    (
        _,
        sdp_master_sim,
        dish_master_sim_1,
        dish_master_sim_2,
    ) = get_master_device_simulators(simulator_factory)

    assert central_node_mid.central_node.ping() > 0
    assert central_node_mid.sdp_master.ping() > 0
    assert central_node_mid.subarray_devices["sdp_subarray"].ping() > 0
    assert sdp_master_sim.ping() > 0
    assert dish_master_sim_1.ping() > 0
    assert dish_master_sim_2.ping() > 0
    if central_node_mid.telescope_state != "ON":
        central_node_mid.csp_master.adminMode = 0
        central_node_mid.wait.set_wait_for_csp_master_to_become_online()
        time.sleep(30)  # Yes, This sleep will be removed.
        central_node_mid.move_to_on()


@given("telescope is in ON state")
def check_telescope_state_is_on(central_node_mid, event_recorder):
    """A method to check if telescopeState is on"""
    event_recorder.subscribe_event(
        central_node_mid.central_node, "telescopeState"
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.central_node,
        "telescopeState",
        DevState.ON,
    )


@when("I standby the telescope")
def move_sdp_to_standby(central_node_mid):
    """A method to put tmc to STANDBY"""
    central_node_mid.set_standby()


@then("the CSP must go to standby state")
def check_csp_is_moved_to_standby(central_node_mid, event_recorder):
    """A method to check CSP's State"""
    event_recorder.subscribe_event(central_node_mid.csp_master, "State")
    event_recorder.subscribe_event(
        central_node_mid.subarray_devices["csp_subarray"], "State"
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.csp_master, "State", DevState.STANDBY, lookahead=15
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_devices["csp_subarray"],
        "State",
        DevState.OFF,
        lookahead=10,
    )
    csp_subarray1 = central_node_mid.subarray_devices["csp_subarray"]
    LOGGER.info("CSPSubarrayState: %s", csp_subarray1.state())


@then("telescope state is STANDBY")
def check_telescope_state_off(central_node_mid, event_recorder):
    """A method to check CentralNode.telescopeState"""
    assert event_recorder.has_change_event_occurred(
        central_node_mid.central_node,
        "telescopeState",
        DevState.STANDBY,
    )
