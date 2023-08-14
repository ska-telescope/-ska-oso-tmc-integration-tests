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
    Test case to verify aggregation for telescopeHealthState.FAILED
    """


@pytest.mark.SKA_mid
@scenario(
    "../features/telescope_health_state_aggregation.feature",
    "Verify TelescopeHealthState as Degraded",
)
def test_telescope_health_state_degraded():
    """
    Test case to verify aggregation for telescopeHealthState.DEGRADED
    """


@pytest.mark.SKA_mid
@scenario(
    "../features/telescope_health_state_aggregation.feature",
    "Verify TelescopeHealthState as Unknown",
)
def test_telescope_health_state_unknown():
    """
    Test case to verify aggregation for telescopeHealthState.UNKNOWN
    """


@given("csp master, sdp master and dish masters health state is OK")
def simulator_devices_health_state_is_ok(simulator_factory, event_recorder):
    """A method to check simulators are in HealthState.OK

    Args:
        simulator_factory: fixture for SimulatorFactory class
        event_recorder: fixture for EventRecorder class
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
    """A method to set HealthState value for the simulator devices

    Args:
        simulator_factory: fixture for SimulatorFactory class
        devices (str): simulator devices
        health_state (str): healthstate value
    """
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
    """A method to check CentralNode.telescopehealthState attribute
    change after aggregation

    Args:
        central_node : A fixture for CentralNode tango device class
        event_recorder: A fixture for EventRecorder class_
        telescope_Health_State (str): telescopehealthState value
    """
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
    """A method to set simulator devices to HealthState.OK

    Args:
        csp_master_sim: Csp Master device sim
        sdp_master_sim: Sdp Master device sim
        dish_master_1: Dish Master 1 device sim
        dish_master_2: Dish Master 2 device sim_
        event_recorder: A fixture for EventRecorder class
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
    """A method to give value of type HealthState
    Args:
        value (str): healthState value as str
    """
    if value == "FAILED":
        return HealthState.FAILED
    elif value == "DEGRADED":
        return HealthState.DEGRADED
    elif value == "UNKNOWN":
        return HealthState.UNKNOWN
