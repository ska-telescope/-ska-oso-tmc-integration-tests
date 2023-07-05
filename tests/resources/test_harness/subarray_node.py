import logging

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
from tests.resources.test_harness.utils.common_utils import JsonFactory
from tests.resources.test_harness.utils.constant import IDLE, ON, READY
from tests.resources.test_harness.utils.enums import DishMode, SubarrayObsState
from tests.resources.test_harness.utils.sync_decorators import (
    sync_abort,
    sync_assign_resources,
    sync_configure,
    sync_end,
    sync_release_resources,
    sync_restart,
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
    "dish_master1": dish_master1,
}


class SubarrayNode(object):
    """
    A TMC SubarrayNode class to implements the standard set
    of commands defined by the SKA Control Model.
    """

    def __init__(self) -> None:
        super().__init__()
        self.subarray_node = DeviceProxy(tmc_subarraynode1)
        self.dish_master_1 = DeviceProxy(dish_master1)
        self._state = DevState.OFF
        # TBD, since ObsState.EMPTY  difficult to import, need a thinking
        self.obs_state = SubarrayObsState.EMPTY
        # setup subarray
        self._setup()
        # Subarray state
        self.ON_STATE = ON
        self.IDLE_OBS_STATE = IDLE
        self.READY_OBS_STATE = READY

    def _setup(self):
        """ """
        self.dish_master_1.SetDirectState(DevState.STANDBY)
        # Setting DishMode to STANDBY_FP
        self.dish_master_1.SetDirectDishMode(DishMode.STANDBY_FP)

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

    def move_to_on(self):
        resource(tmc_subarraynode1).assert_attribute("State").equals("OFF")
        result, message = self.subarray_node.On()
        LOGGER.info("Invoked ON on SubarrayNode")
        return result, message

    def move_to_off(self):
        resource(tmc_subarraynode1).assert_attribute("State").equals("ON")
        result, message = self.subarray_node.Off()
        LOGGER.info("Invoked OFF on SubarrayNode")
        return result, message

    @sync_configure(device_dict=device_dict)
    def configure_subarray(self, input_string):
        result, message = self.subarray_node.Configure(input_string)
        LOGGER.info("Invoked Configure on SubarrayNode")
        return result, message

    @sync_end(device_dict=device_dict)
    def end_observation(self):
        result, message = self.subarray_node.End()
        LOGGER.info("Invoked End on SubarrayNode")
        return result, message

    def invoke_scan(self, input_string):
        result, message = self.subarray_node.Scan(input_string)
        LOGGER.info("Invoked Scan on SubarrayNode")
        return result, message

    @sync_abort(device_dict=device_dict)
    def abort_subarray(self):
        result, message = self.subarray_node.Abort()
        LOGGER.info("Invoked Abort on SubarrayNode")
        return result, message

    @sync_restart(device_dict=device_dict)
    def restart_subarray(self):
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

    def execute_transition(self, command_name, argin=None):
        """
        Args:
            assign_json (_type_): _description_
        """
        result, message = self.subarray_node.command_inout(command_name, argin)
        LOGGER.info(f"Invoked {command_name} on SubarrayNode")
        return result, message

    def force_change_obs_state(self, obs_state_to_change):
        """Force change obs state to provided state
        Args:
            obs_state (str): Obs State
        """
        # TODO: Refactor the given methods, to avoid nested if.
        # low priority item
        json_factory = JsonFactory()
        LOGGER.info(f"Current Obs state is  {self.obs_state}")
        if obs_state_to_change == "IDLE":
            if self.obs_state == "READY":
                # Invoke end command
                self.end_observation()
            elif self.obs_state == "EMPTY":
                # invoke assign_resource
                self.assign_resources_to_subarray(
                    json_factory.create_assign_resource("assign_resources_mid")
                )
        elif obs_state_to_change == "EMPTY":
            if self.obs_state == "IDLE":
                # Invoke Release resource
                self.release_resources_subarray()
            elif self.obs_state == "READY":
                # Invoke End to bring it to IDLE
                # then invoke Release
                self.end_observation()
                self.release_resources_subarray()
        elif obs_state_to_change == "READY":
            if self.obs_state == "EMPTY":
                self.assign_resources_to_subarray(
                    json_factory.create_assign_resource("assign_resources_mid")
                )
                self.configure_subarray(
                    json_factory.create_subarray_configuration("configure_mid")
                )
            elif self.obs_state == "IDLE":
                self.configure_subarray(
                    json_factory.create_subarray_configuration("configure_mid")
                )
            # elif self.obs_state == "SCANNING":
            #     self.end_scanning()
        LOGGER.info(f"Obs state is changed to {self.obs_state}")

    def _reset_mock_devices(self):
        """Reset Mock devices to it's original state"""
        sdp_mock_device = DeviceProxy(sdp_subarray1)
        csp_mock_device = DeviceProxy(csp_subarray1)
        sdp_mock_device.ResetDelay()
        csp_mock_device.ResetDelay()

    def tear_down(self):
        """Tear down after each test run"""

        LOGGER.info("Calling Tear down for subarray")
        if self.obs_state in ("RESOURCING", "CONFIGURING", "SCANNING"):
            """Invoke Abort and Restart"""
            LOGGER.info("Invoking Abort on Subarray")
            self.abort_subarray()
            self.restart_subarray()
        else:
            self.force_change_obs_state("EMPTY")

        # Move Subarray to OFF state
        self.move_to_off()
        self.dish_master_1.SetDirectDishMode(DishMode.STANDBY_LP)
        self.dish_master_1.SetDirectState(DevState.STANDBY)
        self._reset_mock_devices()
