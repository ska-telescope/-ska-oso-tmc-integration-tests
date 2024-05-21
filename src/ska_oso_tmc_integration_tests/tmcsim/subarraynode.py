"""
Simulates the behaviour of a TMC SubArrayNode for integration testing.
"""

import json
from collections import deque

from pydantic import BaseModel, Field
from ska_control_model import ObsState
from statemachine import State
from tango import AttrWriteType, DevState
from tango.server import Device, attribute, command, device_property

from .obsstatestatemachine import ObsStateMachineMixin, ObsStateStateMachine


class MethodCall(BaseModel):
    """
    Simple dataclass for describing a method call on a Tango device server.
    """

    command: str
    args: list = Field(default_factory=list)


class SubArrayNode(Device, ObsStateMachineMixin):
    """
    Simulates the bare minimum TMC SubArrayNode device server functionality
    required for OSO/TMC integration tests.
    """

    state_machine_name = ObsStateStateMachine.name
    state_machine_attr = "statemachine"
    state_field_name = "_obsState"
    initial_state_attr = "initial_obsstate"

    initial_obsstate = device_property(dtype=int)
    """Initial obsState for state machine provided by the OSO test harnesses"""

    history_limit = device_property(dtype=int, default_value=50)
    """
    Maximum size for the call history. The oldest entries will be removed to stay
    below this limit.
    """

    def __init__(self, cl, name):
        Device.__init__(self, cl, name)
        ObsStateMachineMixin.__init__(self)

    def init_device(self):
        """
        Simulate SubArrayNode device initialisation.
        """
        Device.init_device(self)
        # Inform Tango that no polling is required as we'll push obsState change events
        # manually
        self.set_change_event("obsState", True, True)
        # name is used inside on_transition logging message, nowhere else
        self.name = self.get_name()

        self.set_state(DevState.ON)

        self._history: deque[MethodCall] = deque(maxlen=self.history_limit)

    def on_transition(self, event: str, source: State, target: State):
        """
        Template function used by the simulator to hook into statemachine transitions.
        """
        self.info_stream(f"{self.name}: {source.id}--({event})-->{target.id}")
        self.push_change_event("obsState", ObsState(target.value))

    @attribute(dtype=ObsState, access=AttrWriteType.READ)
    def obsState(self) -> ObsState:  # pylint: disable=invalid-name
        """
        Get the current obsState of this SubArrayNode.
        """
        return ObsState(self._obsState)

    @command(dtype_in=str)
    def AssignResources(self, cdm_str):  # pylint: disable=invalid-name
        """Add resources to a subarray."""
        self._history.append(MethodCall(command="AssignResources", args=[cdm_str]))
        self.statemachine.assign_resources(cdm_str)

    @command(dtype_in=str)
    def ReleaseResources(self, cdm_str):  # pylint: disable=invalid-name
        """Release resources from a subarray."""
        self._history.append(MethodCall(command="ReleaseResources", args=[cdm_str]))
        self.statemachine.release_resources(cdm_str)

    @command(dtype_in=str)
    def Configure(self, cdm_str):  # pylint: disable=invalid-name
        """Configure subarray resources."""
        self._history.append(MethodCall(command="Configure", args=[cdm_str]))
        self.statemachine.configure(cdm_str)

    @command(dtype_in=str)
    def Scan(self, cdm_str):  # pylint: disable=invalid-name
        """Perform a scan."""
        self._history.append(MethodCall(command="Scan", args=[cdm_str]))
        self.statemachine.scan(cdm_str)

    @command
    def Abort(self, *args, **kwargs):  # pylint: disable=invalid-name
        """Abort the current operation."""
        self._history.append(MethodCall(command="Abort"))
        self.statemachine.abort(*args, **kwargs)

    @command
    def End(self, *args, **kwargs):  # pylint: disable=invalid-name
        """Mark the end of the scheduling block scan sequence."""
        self._history.append(MethodCall(command="End"))
        self.statemachine.end(*args, **kwargs)

    @command
    def Restart(self, *args, **kwargs):  # pylint: disable=invalid-name
        """Restart the device."""
        self._history.append(MethodCall(command="Restart"))
        self.statemachine.restart(*args, **kwargs)

    @attribute(dtype=str, access=AttrWriteType.READ)
    def History(self) -> str:  # pylint: disable=invalid-name
        """
        Get the history of commands and arguments received by this device.

        The returned JSON string will a serialised list of JSON objects, one
        object for each call received by the device. See the MethodCall class
        for details of the object. The maximum size of the list will match
        the call history size limit, which is set by the history_limit device
        property.

        :return: JSON command history
        """
        history = [h.model_dump() for h in self._history]
        return json.dumps(history)

    @command
    def ClearHistory(self):  # pylint: disable=invalid-name
        """Clear the history of JSON arguments."""
        self._history.clear()
