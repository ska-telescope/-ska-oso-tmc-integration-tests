import logging

from tango import DeviceProxy, DevState

from tests.resources.test_harness.constant import (
    csp_subarray1,
    dish_master1,
    sdp_subarray1,
    tmc_subarraynode1,
)
from tests.resources.test_support.helpers import resource
from tests.resources.test_support.sync_decorators import (
    sync_abort,
    sync_assign_resources,
    sync_configure,
    sync_end,
    sync_release_resources,
    sync_restart,
    sync_scan,
    sync_set_to_off,
    sync_set_to_standby,
    sync_telescope_on,
)

LOGGER = logging.getLogger(__name__)


class SubarrayNode(object):
    """
    A TMC SubarrayNode class to implements the standard set
    of commands defined by the SKA Control Model.
    """

    def __init__(self) -> None:
        self.subarray_node = DeviceProxy(tmc_subarraynode1)
        self.subarray_devices = {
            "csp_subarray": csp_subarray1,
            "sdp_subarray": sdp_subarray1,
            "dish_master": dish_master1,
        }
        self._state = DevState.OFF
        self.obs_state = 0  # TBD, since ObsState.EMPTY  difficult to import, need a thinking

    @property
    def state(self) -> DevState:
        """TMC SubarrayNode operational state"""
        self._state = resource(tmc_subarraynode1).get("State")
        return self._state

    @state.setter
    def state(self, value):
        """Sets value for TMC subarrayNode operational state

        Args:
            value (DevState): operational state value
        """
        self._state = value

    @property
    def obs_state(self):
        """TMC SubarrayNode observation state"""
        self._obs_state = resource(tmc_subarraynode1).get("obsState")
        return self._obs_state

    @obs_state.setter
    def obs_state(self, value):
        """Sets value for TMC subarrayNode observation state

        Args:
            value (DevState): observation state value
        """
        self._obs_state = value

    def invoke_configure(self, input_string):
        resource(tmc_subarraynode1).assert_attribute("State").equals("ON")
        resource(tmc_subarraynode1).assert_attribute("obsState").equals("IDLE")
        result, message = self.subarray_node.Configure(input_string)
        LOGGER.info("Invoked Configure on SubarrayNode")
        return result, message

    def invoke_end(self):
        resource(tmc_subarraynode1).assert_attribute("State").equals("ON")
        resource(tmc_subarraynode1).assert_attribute("obsState").equals(
            "READY"
        )
        result, message = self.subarray_node.End()
        LOGGER.info("Invoked End on SubarrayNode")
        return result, message

    def invoke_scan(self, input_string):
        resource(tmc_subarraynode1).assert_attribute("State").equals("ON")
        resource(tmc_subarraynode1).assert_attribute("obsState").equals(
            "READY"
        )
        result, message = self.subarray_node.Scan(input_string)
        LOGGER.info("Invoked Scan on SubarrayNode")
        return result, message

    def invoke_abort(self):
        resource(tmc_subarraynode1).assert_attribute("State").equals("ON")
        result, message = self.subarray_node.Abort()
        LOGGER.info("Invoked Abort on SubarrayNode")
        return result, message

    def invoke_restart(self):
        resource(tmc_subarraynode1).assert_attribute("State").equals("ON")
        result, message = self.subarray_node.Restart()
        LOGGER.info("Invoked Restart on SubarrayNode")
        return result, message

    # def execute_obsstate_transitions(self, obs_state_value, input_string):
    #     """_summary_

    #     Args:
    #         obs_state_value (_type_): _description_
    #     """
    #     if obs_state_value == "READY":
    #         self.invoke_configure(input_string)
    #     elif obs_state_value == "EMPTY":
    #         if self.obs_state in [0, 1, 2, 3, 4]:
    #             self.invoke_abort()
    #             self.invoke_restart()
    #     elif obs_state_value
