# pylint: disable=redefined-outer-name,missing-module-docstring
from time import time

import pytest
from ska_control_model import ObsState

from ska_oso_tmcsim import ObsStateStateMachine


@pytest.fixture
def sm():
    """Get an instance of an ObsStateStateMachine."""
    return ObsStateStateMachine()


def test_all_states_available(sm):
    """
    Verify that all TMC states can be represented by our simulator.
    """
    for state in ObsState:
        assert hasattr(sm, state.name)


FLOWS = (
    (
        "assign_resources",
        "configure",
        "scan",
        "configure",
        "scan",
        "end",
    ),
    (
        "assign_resources",
        "configure",
    ),
)


@pytest.mark.parametrize("events", FLOWS)
def test_successful_flow(events, sm):
    """
    Verify that we can simulate various flows.
    """
    for evt in events:
        sm.send(evt)


def test_slow_failure(sm):
    """
    Verify that we can simulate a transition that takes too long and then
    eventually fails.
    """
    sm.transition_timing["assign_resources"] = 0.1
    sm.set_to_fail_after(sm.RESOURCING)
    then = time()
    sm.assign_resources({})
    elapsed = time() - then
    assert sm.current_state == sm.FAULT
    assert elapsed == pytest.approx(0.1, abs=0.01)


def test_slow_transitions(sm):
    """
    Verify that we can simulate transitions that take time to complete.
    """
    sm.transition_timing["assign_resources"] = 0.2
    sm.transition_timing["scan"] = 0.3
    then = time()
    sm.assign_resources({})
    sm.configure()
    sm.scan()
    sm.end()
    elapsed = time() - then
    assert elapsed == pytest.approx(0.5, abs=0.01)


def test_fault_single(sm):
    """Verify that we can simulate failures as soon as a given state is encountered"""
    sm.set_to_fail_after(sm.IDLE)
    sm.assign_resources()
    assert sm.current_state == sm.FAULT


def test_fault_whole_history(sm):
    """Verify that we can simulate failures passing an entire history."""
    sm.set_to_fail_after(sm.EMPTY, sm.RESOURCING, sm.IDLE, sm.CONFIGURING)
    sm.assign_resources()
    assert sm.current_state != sm.FAULT
    sm.configure()  # Fails on the internal transition from CONFIGURING->READY
    assert sm.current_state == sm.FAULT


def test_fault_specific_pattern(sm):
    """Verify that we can do whatever we want until the specific pattern that triggers
    a simulated failure."""
    # Double configure, fails after next scanning
    sm.set_to_fail_after(
        sm.CONFIGURING, sm.READY, sm.CONFIGURING, sm.READY, sm.SCANNING
    )
    sm.assign_resources()
    # These are fine...
    sm.configure()
    sm.scan()
    sm.scan()
    sm.scan()
    assert sm.current_state != sm.FAULT
    # ...but now it goes wrong:
    sm.configure()
    sm.configure()
    sm.scan()
    assert sm.current_state == sm.FAULT


def test_fault_injection_works_before_internal_transitions(sm):
    """
    For an action like configure, the action will transition from IDLE -> CONFIGURING
    and then an 'after' hook will call the ready action causing CONFIGURING -> READY.

    If we inject a fault after ['IDLE', 'CONFIGURING'], we want to ensure the FAULT
    transition happens before the transition to READY.
    """

    sm.set_to_fail_after(sm.IDLE, sm.CONFIGURING)
    sm.assign_resources()

    sm.configure()

    assert sm.READY not in sm.state_history
    assert sm.current_state == sm.FAULT
