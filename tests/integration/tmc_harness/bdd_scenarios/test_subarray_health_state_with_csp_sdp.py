"""Test Subarray Health State
"""
import pytest
from pytest_bdd import given, parsers, scenario, then, when
from ska_tango_base.control_model import HealthState

from tests.resources.test_harness.helpers import (
    get_device_simulator_with_given_name,
    get_device_simulators,
)


@pytest.mark.invalid
@pytest.mark.SKA_mid
@scenario(
    "../features/test_harness/subarray_health_state.feature",
    "Subarray Health State should be Failed or Degraded when one or more "
    "devices health state is Failed or Degraded",
)
def test_subarray_health_state(subarray_node):
    """
    Test Subarray Health is Failed or degraded when
    """


@given("csp subarray, sdp subarray and dish masters health state is OK")
def given_simulator_device_health_state_is_ok(simulator_factory):
    """ """
    (
        csp_sa_sim,
        sdp_sa_sim,
        dish_master_1,
        dish_master_2,
    ) = get_device_simulators(simulator_factory)

    csp_sa_sim.SetDirectHealthState(HealthState.OK)
    sdp_sa_sim.SetDirectHealthState(HealthState.OK)
    dish_master_1.SetDirectHealthState(HealthState.OK)
    dish_master_2.SetDirectHealthState(HealthState.OK)


@when(
    parsers.parse(
        "The {Devices} health state changes to {Device_Health_State}"
    )
)
def set_devices_health_state(simulator_factory, Devices, Device_Health_State):
    """Set Devices health state as per provided argument"""
    # Get simulator device objects
    from tests.conftest import LOGGER
    devices = Devices.split(",")
    LOGGER.info("Devices List %s", devices)
    device_simulator_list = get_device_simulator_with_given_name(
        simulator_factory, devices
    )
    LOGGER.info("Devices List 1 %s", device_simulator_list)
    # Set Device Health State
    health_state_list = Device_Health_State.split(",")
    for device_simulator, device_health_state in zip(
        device_simulator_list, health_state_list
    ):
        device_simulator.SetDirectHealthState(HealthState[device_health_state])


@then(parsers.parse("subarray health state is {Subarray_Health_State}"))
def validate_expected_subarray_health_state(
    subarray_node, event_recorder, Subarray_Health_State
):
    """Validate Expected Health state for Subarray Node"""
    event_recorder.subscribe_event(subarray_node.subarray_node, "healthState")
    # Subarray node react automatically
    assert event_recorder.has_change_event_occurred(
        subarray_node.subarray_node,
        "healthState",
        HealthState[Subarray_Health_State],
    ), f"Expected Subarray Node HealthState to be {Subarray_Health_State}"
