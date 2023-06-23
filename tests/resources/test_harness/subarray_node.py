import logging
from os.path import dirname, join

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
    sync_endscan,
    sync_release_resources,
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


def get_subarray_assign_json():
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
    return assign_json


def get_configure_json():
    configure_file_path = join(
        dirname(__file__),
        "..",
        "..",
        "data",
        "command_Configure.json",  # TODO Get this json based on mid or low
    )
    with open(configure_file_path, "r", encoding="UTF-8") as f:
        assign_json = f.read()
    return assign_json


class SubarrayNode(object):
    """
    A TMC SubarrayNode class to implements the standard set
    of commands defined by the SKA Control Model.
    """

    def __init__(self) -> None:
        super().__init__()
        self.subarray_node = DeviceProxy(tmc_subarraynode1)
        self._state = DevState.OFF
        # TBD, since ObsState.EMPTY  difficult to import, need a thinking
        self.obs_state = 0
        # setup subarray
        self._setup()

    def _setup(self):
        """ """
        dish_master_1 = DeviceProxy(dish_master1)
        dish_master_1.SetDirectState(DevState.STANDBY)
        # Setting DishMode to STANDBY_FP
        dish_master_1.SetDirectDishMode(3)

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
        resource(tmc_subarraynode1).assert_attribute("State").equals("ON")
        resource(tmc_subarraynode1).assert_attribute("obsState").equals("IDLE")
        result, message = self.subarray_node.Configure(input_string)
        LOGGER.info("Invoked Configure on SubarrayNode")
        return result, message

    @sync_end(device_dict=device_dict)
    def end_observation(self):
        resource(tmc_subarraynode1).assert_attribute("State").equals("ON")
        resource(tmc_subarraynode1).assert_attribute("obsState").equals(
            "READY"
        )
        result, message = self.subarray_node.End()
        LOGGER.info("Invoked End on SubarrayNode")
        return result, message

    @sync_endscan(device_dict)
    def end_scanning(self):
        """ """
        result, message = self.subarray_node.EndScan()
        LOGGER.info("Invoked End Scan on SubarrayNode")
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
    def assign_resources_to_subarray(self, assign_json, device_dict=None):
        """
        Args:
            assign_json (_type_): _description_
        """
        result, message = self.subarray_node.AssignResources(assign_json)
        LOGGER.info("Invoked AssignResources on SubarrayNode")
        return result, message

    @sync_release_resources(device_dict)
    def release_resources_subarray(self):
        """
        Args:
            assign_json (_type_): _description_
        """
        result, message = self.subarray_node.ReleaseAllResources()
        LOGGER.info("Invoked Release Resource on SubarrayNode")
        return result, message

    def force_change_obs_state(self, obs_state_to_change):
        """Force change obs state to provided state
        Args:
            obs_state (str): Obs State
        """
        LOGGER.info(f"Current Obs state is  {self.obs_state}")
        if obs_state_to_change == "IDLE":
            if self.obs_state == "READY":
                # Invoke end command
                self.end_observation()
            elif self.obs_state == "EMPTY":
                # invoke assign_resource
                self.assign_resources_to_subarray(get_subarray_assign_json())
        elif obs_state_to_change == "EMPTY":
            if self.obs_state == "IDLE":
                # Invoke Release resource
                self.release_resources_subarray()
            elif self.obs_state == "READY":
                # Invoke End to bring it to IDLE and then invoke Release
                self.end_observation()
                self.release_resources_subarray()
        elif obs_state_to_change == "READY":
            if self.obs_state == "EMPTY":
                self.assign_resources_to_subarray(get_subarray_assign_json())
                self.invoke_configure(get_configure_json())
            elif self.obs_state == "IDLE":
                self.invoke_configure(get_configure_json())
            elif self.obs_state == "SCANNING":
                self.end_scanning()
        LOGGER.info(f"Obs state is changed to {self.obs_state}")
