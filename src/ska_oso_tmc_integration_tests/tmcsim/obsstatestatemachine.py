"""
obsstatemachine encodes the ADR-8 Subarray state model into a
"""

import json
from json import JSONDecodeError
from time import sleep
from typing import Any, Optional

from ska_control_model import ObsState
from statemachine import State, StateMachine, registry
from statemachine.i18n import _
from statemachine.states import States


class ObsStateMachineMixin:  # pylint: disable=too-few-public-methods
    """This mixin extends the default statemachine MachineMixin to allow
    setting of the state machine's initial state. This specialisation only
    handles obsStates and expects the initial state to be set via a Tango
    device property.
    """

    state_field_name = "state"  # type: str
    """The model's state field name that will hold the state value."""

    state_machine_name = None  # type: str
    """A fully qualified name of the class, where it can be imported."""

    state_machine_attr = "statemachine"  # type: str
    """Name of the model's attribute that will hold the machine instance."""

    initial_state_attr = "initial_state"  # type: str
    """Name of the device property that holds the desired initial state machine state.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.state_machine_name:
            raise ValueError(
                _("{!r} is not a valid state machine name.").format(
                    self.state_machine_name
                )
            )
        machine_cls = registry.get_machine_cls(self.state_machine_name)

        # this property should be set on the device
        initial_int_obsstate = getattr(self, self.initial_state_attr)
        assert initial_int_obsstate is not None, f"{self.initial_state_attr} not set"

        # map int back to ObsState state value
        idx_to_state = {s.value: s for s in BaseObsStateMachine._states}
        initial_obsstate = idx_to_state[initial_int_obsstate].value

        setattr(
            self,
            self.state_machine_attr,
            machine_cls(
                self,
                start_value=initial_obsstate,
                state_field=self.state_field_name,
            ),
        )


class BaseObsStateMachine(StateMachine):
    """
    Simple state machine for tracking SubArrayNode transitions as defined in ADR-8.

    https://confluence.skatelescope.org/x/bIdIBg
    """

    # Use the real Subarray states from the SKA control model
    _states = States.from_enum(ObsState, initial=ObsState.EMPTY)

    # the states are copied into root just to make transition definition easier
    EMPTY = _states.EMPTY
    RESOURCING = _states.RESOURCING
    IDLE = _states.IDLE
    CONFIGURING = _states.CONFIGURING
    READY = _states.READY
    SCANNING = _states.SCANNING
    ABORTING = _states.ABORTING
    ABORTED = _states.ABORTED
    FAULT = _states.FAULT
    RESTARTING = _states.RESTARTING
    RESETTING = _states.RESETTING

    # actions. These are all the commands that a user can invoke.
    assign_resources = EMPTY.to(RESOURCING, after="assigned") | IDLE.to(
        RESOURCING, after="assigned"
    )
    release_resources = IDLE.to(RESOURCING, after="released")
    configure = IDLE.to(CONFIGURING, after="ready") | READY.to(
        CONFIGURING, after="ready"
    )
    end = READY.to(IDLE)
    scan = READY.to(SCANNING, after="scan_complete")
    # Will never be called by OSO. Also, because scan() is hardcoded to
    # after='scan_complete'
    end_scan = SCANNING.to(READY)
    reset = ABORTED.to(RESETTING, after="reset_complete") | FAULT.to(
        RESETTING, after="reset_complete"
    )
    abort = (
        RESOURCING.to(ABORTING, after="abort_complete")
        | IDLE.to(ABORTING, after="abort_complete")
        | CONFIGURING.to(ABORTING, after="abort_complete")
        | READY.to(ABORTING, after="abort_complete")
        | SCANNING.to(ABORTING, after="abort_complete")
    )
    restart = ABORTED.to(RESTARTING, after="restart_complete") | FAULT.to(
        RESTARTING, after="restart_complete"
    )

    # internal transitions triggered by downstream device state
    assigned = RESOURCING.to(IDLE)
    released = RESOURCING.to(EMPTY, cond="is_release_all") | RESOURCING.to(
        IDLE, unless="is_release_all"
    )
    ready = CONFIGURING.to(READY)
    scan_complete = SCANNING.to(READY)
    abort_complete = ABORTING.to(ABORTED)
    restart_complete = RESTARTING.to(EMPTY)

    fatal_error = (
        EMPTY.to(FAULT)
        | RESOURCING.to(FAULT)
        | IDLE.to(FAULT)
        | CONFIGURING.to(FAULT)
        | READY.to(FAULT)
        | SCANNING.to(FAULT)
        | ABORTING.to(FAULT)
        | ABORTED.to(FAULT)
        | RESTARTING.to(FAULT)
        | RESETTING.to(FAULT)
    )
    reset_complete = RESETTING.to(IDLE)

    def is_release_all(self, cdm_json):
        """
        Guard to detect whether a JSON string includes the term 'release_all'.

        The end state for ReleaseResources is different depending on whether the
        payload contains 'release_all' or not. This guard is used to find the desired
        end state.

        :param cdm_json: JSON to analyse
        :return: True if 'release_all' in JSON.
        """
        try:
            cdm_dict = json.loads(cdm_json)
        except (TypeError, JSONDecodeError):
            cdm_dict = {}
        return cdm_dict.get("release_all", False)


class ObsStateStateMachine(BaseObsStateMachine):
    """
    State machine that encodes the transitions in the ADR-8 subarray state model.
    """

    default_transition_time = 0

    def __init__(  # pylint: disable=too-many-arguments
        self,
        model: Any = None,
        state_field: str = "state",
        start_value: Any = None,
        rtc: bool = True,
        allow_event_without_transition: bool = False,
        transition_timing: Optional[dict[str, int | float]] = None,
    ):
        self.transition_timing = (
            transition_timing if transition_timing is not None else {}
        )
        self._fail_after = None
        self.state_history = []
        super().__init__(
            model,
            state_field,
            start_value,
            rtc,
            allow_event_without_transition,
        )

    def set_to_fail_after(self, *states: State):
        """
        Primes a transition to FAULT after a state sequence matching the input state
        sequence.

        :param states: state sequence to match
        """
        self._fail_after = list(states)

    def on_enter_state(self, state):
        """
        Perform actions that should occur on entering a new state.

        This template function hooks into python-statemachine and is called whenever a
        new state is entered.

        :param state: new state
        """
        self.state_history.append(state)

    def after_transition(self, event):
        """
        Perform actions that should occur after a state transition.

        This template function hooks into python-statemachine and is called whenever a
        state transition has completed.

        :param event: state transition that occurred
        """
        sleep_seconds = self.transition_timing.get(event, self.default_transition_time)
        sleep(sleep_seconds)
        if (
            self._fail_after
            and self.state_history[-len(self._fail_after) :] == self._fail_after
        ):
            self.fatal_error()


class LoggingObserver:  # pylint: disable=too-few-public-methods
    """
    State machine observer that logs every transition. Useful for development and
    testing.

    See https://python-statemachine.readthedocs.io/en/latest/observers.html
    """

    def on_transition(self, event: str, source: State, target: State):
        """
        Logs state transitions as and when they occur.
        """
        print(f"{source.id}--({event})-->{target.id}")


if __name__ == "__main__":
    # This code is just a way to run the state machine through a few transitions.
    # It is not intended to ever be run in production. Feel free to modify this
    # with your own transitions if you want to see/test how the machine works.
    m = ObsStateStateMachine()
    m.add_observer(LoggingObserver())
    FAKE_JSON = "{}"
    m.assign_resources(FAKE_JSON)
    m.configure(FAKE_JSON)
    m.scan(FAKE_JSON)
    m.configure(FAKE_JSON)
    m.scan(FAKE_JSON)
    m.configure(FAKE_JSON)
    m.scan(FAKE_JSON)
    m.end(FAKE_JSON)
    m.release_resources(json.dumps({"release_all": True}))
