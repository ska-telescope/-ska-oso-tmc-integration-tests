import pytest
from pytest_bdd import given, parsers, scenario, then, when
from ska_tango_base.control_model import HealthState

from tests.resources.test_harness.helpers import (
    get_device_simulator_with_given_name,
    get_master_device_simulators,
)


@pytest.mark.SKA_mid
@scenario(
    "../features/telescope_health_state_aggregation.feature",
    "Verify TelescopeHealthState as Failed",
)
def test_telescope_health_state_failed():
    """
    Test case to verify aggregation for telescopHealthState.FAILED
    """


@pytest.mark.SKA_mid
@scenario(
    "../features/telescope_health_state_aggregation.feature",
    "Verify TelescopeHealthState as Degraded",
)
def test_telescope_health_state_degraded():
    """
    Test case to verify aggregation for telescopHealthState.DEGRADED
    """


@pytest.mark.SKA_mid
@scenario(
    "../features/telescope_health_state_aggregation.feature",
    "Verify TelescopeHealthState as Unknown",
)
def test_telescope_health_state_unknown():
    """
    Test case to verify aggregation for telescopHealthState.UNKNOWN
    """


@given("csp master, sdp master and dish masters health state is OK")
def simulator_devices_health_state_is_ok(simulator_factory, event_recorder):
    """_summary_

    Args:
        simulator_factory (_type_): _description_
        event_recorder (_type_): _description_
    """
    (
        csp_master_sim,
        sdp_master_sim,
        dish_master_1,
        dish_master_2,
    ) = get_master_device_simulators(simulator_factory)
    set_simulators_health_state_as_ok(
        csp_master_sim,
        sdp_master_sim,
        dish_master_1,
        dish_master_2,
        event_recorder,
    )

    assert event_recorder.has_change_event_occurred(
        csp_master_sim, "healthState", HealthState.OK
    ), "Expected HealthState to be OK"
    assert event_recorder.has_change_event_occurred(
        sdp_master_sim, "healthState", HealthState.OK
    ), "Expected HealthState to be OK"
    assert event_recorder.has_change_event_occurred(
        dish_master_1, "healthState", HealthState.OK
    ), "Expected HealthState to be OK"
    assert event_recorder.has_change_event_occurred(
        dish_master_2, "healthState", HealthState.OK
    ), "Expected HealthState to be OK"


@when(parsers.parse("The {devices} health state changes to {health_state}"))
def simulator_device_health_state_changes(
    simulator_factory, devices, health_state
):
    devices_list = devices.split(",")
    health_state_list = health_state.split(",")

    sim_devices_list = get_device_simulator_with_given_name(
        simulator_factory, devices_list
    )
    for simulator_device, health_state_val in list(
        zip(sim_devices_list, health_state_list)
    ):
        health_state = get_enum(health_state_val)
        simulator_device.SetDirectHealthState(health_state)


@then(parsers.parse("the telescope health state is {telescope_Health_State}"))
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
    ), f"Expected telescopeHealthState to be {health_state}"


def set_simulators_health_state_as_ok(
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
    elif value == "DEGRADED":
        return HealthState.DEGRADED
    elif value == "UNKNOWN":
        return HealthState.UNKNOWN
