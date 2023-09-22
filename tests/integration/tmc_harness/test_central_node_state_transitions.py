import pytest
from tango import DevState

from tests.resources.test_harness.central_node_mid import CentralNodeWrapperMid
from tests.resources.test_harness.helpers import get_master_device_simulators


def test_centralnode_state_transitions_valid_data(
    central_node,
    event_recorder,
    simulator_factory,
):
    """
    Test to verify transitions that are triggered by On and Off
    command and followed by a completion transition
    assuming that external subsystems work fine.
    Glossary:
    - "central_node": fixture for a TMC CentralNode Mid/Low under test
    which provides simulated master devices
    - "event_recorder": fixture for a MockTangoEventCallbackGroup
    for validating the subscribing and receiving events.
    - "simulator_factory": fixtur for creating simulator devices for
    low and mid Telescope respectively.
    """
    (
        csp_master_sim,
        sdp_master_sim,
        dish_master_sim1,
        dish_master_sim2,
    ) = get_master_device_simulators(simulator_factory)

    event_recorder.subscribe_event(csp_master_sim, "State")
    event_recorder.subscribe_event(sdp_master_sim, "State")
    central_node.move_to_on()

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
    if type(central_node) == CentralNodeWrapperMid:
        event_recorder.subscribe_event(dish_master_sim1, "State")
        event_recorder.subscribe_event(dish_master_sim2, "State")
        assert event_recorder.has_change_event_occurred(
            dish_master_sim1,
            "State",
            DevState.STANDBY,
        )
        assert event_recorder.has_change_event_occurred(
            dish_master_sim2,
            "State",
            DevState.STANDBY,
        )
    central_node.set_off()
    assert event_recorder.has_change_event_occurred(
        csp_master_sim,
        "State",
        DevState.OFF,
    )
    assert event_recorder.has_change_event_occurred(
        sdp_master_sim,
        "State",
        DevState.OFF,
    )


@pytest.mark.deployment("LOW")
@pytest.mark.SKA_low
def test_low_centralnode_state_transitions_valid_data(
    central_node, event_recorder, simulator_factory
):
    """Test for checking the state transition for low Low Telescope"""
    test_centralnode_state_transitions_valid_data(
        central_node,
        event_recorder,
        simulator_factory,
    )


@pytest.mark.SKA_mid
def test_mid_centralnode_state_transitions_valid_data(
    central_node, event_recorder, simulator_factory
):
    """Test for checking the state transition for low Low Telescope"""
    test_centralnode_state_transitions_valid_data(
        central_node,
        event_recorder,
        simulator_factory,
    )
