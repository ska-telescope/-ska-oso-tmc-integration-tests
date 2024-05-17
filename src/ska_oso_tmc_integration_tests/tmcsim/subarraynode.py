"""
Simulates the behaviour of a TMC SubArrayNode for integration testing.
"""

from ska_control_model import ObsState
from statemachine import State
from tango import AttrWriteType, DevState
from tango.server import Device, attribute, command, device_property

from .obsstatestatemachine import ObsStateMachineMixin, ObsStateStateMachine


class SubArrayNode(ObsStateMachineMixin, Device):
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
        self.statemachine.assign_resources(cdm_str)

    @command(dtype_in=str)
    def ReleaseResources(self, cdm_str):  # pylint: disable=invalid-name
        """Release resources from a subarray."""
        self.statemachine.release_resources(cdm_str)

    @command(dtype_in=str)
    def Configure(self, cdm_str):  # pylint: disable=invalid-name
        """Configure subarray resources."""
        self.statemachine.configure(cdm_str)

    @command(dtype_in=str)
    def Scan(self, cdm_str):  # pylint: disable=invalid-name
        """Perform a scan."""
        self.statemachine.scan(cdm_str)

    @command
    def Abort(self, *args, **kwargs):  # pylint: disable=invalid-name
        """Abort the current operation."""
        self.statemachine.abort(*args, **kwargs)

    @command
    def End(self, *args, **kwargs):  # pylint: disable=invalid-name
        """Mark the end of the scheduling block scan sequence."""
        self.statemachine.end(*args, **kwargs)

    @command
    def Restart(self, *args, **kwargs):  # pylint: disable=invalid-name
        """Restart the device."""
        self.statemachine.restart(*args, **kwargs)
