import logging
from os.path import abspath, dirname, join

from tango import DeviceProxy, DevState

from tests.resources.test_harness.constant import (
    centralnode,
    csp_master,
    csp_subarray1,
    dish_master1,
    sdp_master,
    sdp_subarray1,
    tmc_subarraynode1,
)
from tests.resources.test_harness.utils.sync_decorators import (
    sync_assign_resources,
    sync_configure,
    sync_end,
)
from tests.resources.test_support.helpers import resource

LOGGER = logging.getLogger(__name__)

device_dict = {
    # TODO use this as as list when multiple subarray considered in testing
    "sdp_subarray": sdp_subarray1,
    "csp_subarray": csp_subarray1,
    "csp_master": csp_master,
    "tmc_subarraynode": tmc_subarraynode1,
    "sdp_master": sdp_master,
    "centralnode": centralnode,
}


class SubarrayNode(object):
    """
    A TMC SubarrayNode class to implements the standard set
    of commands defined by the SKA Control Model.
    """

    def __init__(self) -> None:
        super().__init__()
        self.subarray_node = DeviceProxy(tmc_subarraynode1)
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

    @sync_configure(device_dict=device_dict)
    def invoke_configure(self, input_string):
        dish_master_1 = DeviceProxy(dish_master1)
        dish_master_1.SetDirectState(DevState.STANDBY)
        # Setting DishMode to STANDBY_FP
        dish_master_1.SetDirectDishMode(3)
        resource(tmc_subarraynode1).assert_attribute("State").equals("ON")
        resource(tmc_subarraynode1).assert_attribute("obsState").equals("IDLE")
        result, message = self.subarray_node.Configure(input_string)
        LOGGER.info("Invoked Configure on SubarrayNode")
        return result, message

    @sync_end(device_dict=device_dict)
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

    @sync_assign_resources(device_dict)
    def invoke_assign_resources(self, assign_json, device_dict=None):
        """
        Args:
            assign_json (_type_): _description_
        """
        result, message = self.subarray_node.AssignResources(assign_json)
        LOGGER.info("Invoked AssignResources on SubarrayNode")
        return result, message

    def force_change_obs_state(self, obs_state_to_change):
        """Force change obs state to provided state
        Args:
            obs_state (str): Obs State
        """
        if obs_state_to_change == "IDLE":
            if self.obs_state == "READY":
                # Invoke end command
                self.invoke_end()
            elif self.obs_state == "EMPTY":
                # invoke assign_resource
                assign_json_file_path = join(
                    dirname(__file__),
                    "..",
                    "..",
                    "data",
                    "subarray",
                    "assign_resource_mid.json",  # TODO Get this json based on mid or low
                )
                with open(assign_json_file_path, "r", encoding="UTF-8") as f:
                    assign_json = f.read()
                self.invoke_assign_resources(assign_json)
        # TODO handle other obs state
