import logging

from ska_tango_base.control_model import HealthState
from tango import DevState

from tests.resources.test_support.common_utils.common_helpers import Resource

LOGGER = logging.getLogger(__name__)


# TODO ::
# This class needs to be enhanced as a part of upcoming
# Test harness work


class BaseNodeWrapper(object):

    """A wrapper class to implement common tango specific details
    and standard set of commands for TMC
    defined by the SKA Control Model.
    """

    def __init__(
        self,
    ) -> None:
        self.central_node = None
        self.subarray_node = None
        self.csp_master_leaf_node = None
        self.sdp_master_leaf_node = None
        self.mccs_master_leaf_node = None
        self.subarray_devices = {}
        self.sdp_master = None
        self.csp_master = None
        self.mccs_master = None
        self.dish_master_list = None
        self._state = DevState.OFF

    def move_to_on(self) -> NotImplementedError:
        """
        Abstract method for move_to_on
        """
        raise NotImplementedError("To be defined in the lower level classes")


class CentralNodeWrapper(BaseNodeWrapper):
    """A wrapper class to implement common tango specific details
    and standard set of commands for TMC CentralNode,
    defined by the SKA Control Model.
    """

    def __init__(
        self,
    ) -> None:
        super().__init__()

    @property
    def state(self) -> DevState:
        """TMC CentralNode operational state"""
        self._state = Resource(self.central_node).get("State")
        return self._state

    @state.setter
    def state(self, value):
        """Sets value for TMC CentralNode operational state

        Args:
            value (DevState): operational state value
        """
        self._state = value

    @property
    def telescope_health_state(self) -> HealthState:
        """Telescope health state representing overall health of telescope"""
        self._telescope_health_state = Resource(self.central_node).get(
            "telescopeHealthState"
        )
        return self._telescope_health_state

    @telescope_health_state.setter
    def telescope_health_state(self, value):
        """Telescope health state representing overall health of telescope

        Args:
            value (HealthState): telescope health state value
        """
        self._telescope_health_state = value

    @property
    def telescope_state(self) -> DevState:
        """Telescope state representing overall state of telescope"""

        self._telescope_state = Resource(self.central_node).get(
            "telescopeState"
        )
        return self._telescope_state

    @telescope_state.setter
    def telescope_state(self, value):
        """Telescope state representing overall state of telescope

        Args:
            value (DevState): telescope state value
        """
        self._telescope_state = value

    def move_to_on(self) -> NotImplementedError:
        """
        Abstract method for move_to_on
        """
        raise NotImplementedError("To be defined in the lower level classes")

    def move_to_off(self):
        """
        Abstract method for move_to_off
        """
        raise NotImplementedError("To be defined in the lower level classes")

    def set_standby(self):
        """
        Abstract method for move_to_standby
        """
        raise NotImplementedError("To be defined in the lower level classes")

    def store_resources(self):
        """
        Abstract method for invoking AssignResources()
        """
        raise NotImplementedError("To be defined in the lower level classes")

    def invoke_release_resources(self):
        """
        Abstract method for invoking ReleaseResources()
        """
        raise NotImplementedError("To be defined in the lower level classes")
