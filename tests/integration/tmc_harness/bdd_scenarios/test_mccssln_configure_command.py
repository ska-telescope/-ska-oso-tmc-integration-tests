import pytest
from pytest_bdd import given, scenario
from ska_control_model import ObsState
from tango import DevState


@pytest.mark.bdd_assign
@pytest.mark.SKA_mid
@scenario(
    "../features/check_configure_command.feature",
    "TMC executes Configure command successfully.",
)
def test_mccssln_configure_command():
    """ """


@given("a TMC")
def given_tmc(central_node_mid, event_recorder):
    event_recorder.subscribe_event(
        central_node_mid.central_node, "telescopeState"
    )
    event_recorder.subscribe_event(central_node_mid.subarray_node, "obsState")
    central_node_mid.move_to_on()
    assert event_recorder.has_change_event_occurred(
        central_node_mid.central_node,
        "telescopeState",
        DevState.ON,
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.subarray_node,
        "obsState",
        ObsState.EMPTY,
    )
