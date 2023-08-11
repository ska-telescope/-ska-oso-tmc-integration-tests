import pytest
from pytest_bdd import given, parsers, scenario, then, when
from ska_tango_base.control_model import HealthState

from tests.resources.test_harness.helpers import (
    get_device_simulator_with_given_name,
    get_master_device_simulators,
)


@pytest.mark.bdd
@pytest.mark.SKA_mid
@scenario(
    "../features/telescope_health_state_aggregation.feature",
    "Verify TelescopeHealthState as Failed",
)
def test_tmc_telescope_health_state():
    """
    Test cases to verify telescopHealthState aggregation
    """


@given("csp master, sdp master and dish masters health state is OK")
def master_devices_healthstate_is_ok(simulator_factory, event_recorder):
    (
        csp_master_sim,
        sdp_master_sim,
        dish_master_1,
        dish_master_2,
    ) = get_master_device_simulators(simulator_factory)
    set_health_state_as_ok(
        csp_master_sim,
        sdp_master_sim,
        dish_master_1,
        dish_master_2,
        event_recorder,
    )

    assert event_recorder.has_change_event_occurred(
        csp_master_sim, "healthState", HealthState.OK
    ), "Expected Telescope HealthState to be OK"
    assert event_recorder.has_change_event_occurred(
        sdp_master_sim, "healthState", HealthState.OK
    ), "Expected Telescope HealthState to be OK"
    assert event_recorder.has_change_event_occurred(
        dish_master_1, "healthState", HealthState.OK
    ), "Expected Telescope HealthState to be OK"
    assert event_recorder.has_change_event_occurred(
        dish_master_2, "healthState", HealthState.OK
    ), "Expected Telescope HealthState to be OK"


@when(parsers.parse("{devices} health state is {Health_State}"))
def device_health_state_change_to_failed(
    simulator_factory, devices, Health_State
):
    devices_list = devices.split(",")
    sim_devices_list = get_device_simulator_with_given_name(
        simulator_factory, devices_list
    )
    print(sim_devices_list)
    health_state_list = Health_State.split(",")
    print(health_state_list)
    devices_with_health_states = list(zip(sim_devices_list, health_state_list))
    print(devices_with_health_states)
    for device, health_state_val in devices_with_health_states:
        # health_state_val = HealthState(health_state_val)
        health_state = get_enum(health_state_val)
        device.SetDirectHealthState(health_state)


@then(
    parsers.parse("the TMC telescope health state is {telescope_Health_State}")
)
def check_telescope_health_state(
    central_node, event_recorder, telescope_Health_State
):
    health_state = get_enum(telescope_Health_State)
    event_recorder.subscribe_event(
        central_node.central_node, "telescopeHealthState"
    )

    assert event_recorder.has_change_event_occurred(
        central_node.central_node,
        "telescopeHealthState",
        health_state,
    )


def set_health_state_as_ok(
    csp_master_sim,
    sdp_master_sim,
    dish_master_1,
    dish_master_2,
    event_recorder,
):
    """_summary_

    Args:
        csp_master_sim (_type_): _description_
        sdp_master_sim (_type_): _description_
        dish_master_1 (_type_): _description_
        dish_master_2 (_type_): _description_
        event_recorder (_type_): _description_
    """
    event_recorder.subscribe_event(csp_master_sim, "healthState")
    event_recorder.subscribe_event(sdp_master_sim, "healthState")
    event_recorder.subscribe_event(dish_master_1, "healthState")
    event_recorder.subscribe_event(dish_master_2, "healthState")
    csp_master_sim.SetDirectHealthState(HealthState.OK)
    sdp_master_sim.SetDirectHealthState(HealthState.OK)
    dish_master_1.SetDirectHealthState(HealthState.OK)
    dish_master_2.SetDirectHealthState(HealthState.OK)


def get_enum(value):
    """_summary_

    Args:
        value (_type_): _description_
    """
    if value == "FAILED":
        return HealthState.FAILED
