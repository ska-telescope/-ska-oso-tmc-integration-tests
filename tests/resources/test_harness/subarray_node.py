import logging

from tango import DeviceProxy, DevState

from tests.resources.test_harness.constant import (
    centralnode,
    csp_master,
    csp_subarray1,
    dish_master1,
    dish_master2,
    sdp_master,
    sdp_subarray1,
    tmc_subarraynode1,
)
from tests.resources.test_harness.utils.constant import (
    ABORTED,
    IDLE,
    ON,
    READY,
)
from tests.resources.test_harness.utils.enums import DishMode, SubarrayObsState
from tests.resources.test_harness.utils.state_resetter import (
    ObsStateResetterFactory,
)
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
    "dish_master2": dish_master2,
}


class SubarrayNode(object):
    """
    A TMC SubarrayNode class to implements the standard set
    of commands defined by the SKA Control Model.
    """

    def __init__(self) -> None:
        super().__init__()
        self.subarray_node = DeviceProxy(tmc_subarraynode1)
        self.dish_master_list = [
            DeviceProxy(dish_master1),
            DeviceProxy(dish_master2),
        ]

        self._state = DevState.OFF
        # TBD, since ObsState.EMPTY  difficult to import, need a thinking
        self.obs_state = SubarrayObsState.EMPTY
        # setup subarray
        self._setup()
        # Subarray state
        self.ON_STATE = ON
        self.IDLE_OBS_STATE = IDLE
        self.READY_OBS_STATE = READY
        self.ABORTED_OBS_STATE = ABORTED

    def _setup(self):
        """ """
        for dish_master_proxy in self.dish_master_list:
            dish_master_proxy.SetDirectState(DevState.STANDBY)
            # Setting DishMode to STANDBY_FP
            dish_master_proxy.SetDirectDishMode(DishMode.STANDBY_FP)

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
        if self.state != self.ON_STATE:
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
    def store_configuration_data(self, input_string):
        result, message = self.subarray_node.Configure(input_string)
        LOGGER.info("Invoked Configure on SubarrayNode")
        return result, message

    @sync_end(device_dict=device_dict)
    def end_observation(self):
        result, message = self.subarray_node.End()
        LOGGER.info("Invoked End on SubarrayNode")
        return result, message

    def store_scan_data(self, input_string):
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
    def store_resources(self, assign_json):
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
        if command_name is not None:
            result, message = self.subarray_node.command_inout(
                command_name, argin
            )
            LOGGER.info(f"Invoked {command_name} on SubarrayNode")
            return result, message

    def _reset_mock_devices(self):
        """Reset Mock devices to it's original state"""
        for mock_device_fqdn in [sdp_subarray1, csp_subarray1]:
            device = DeviceProxy(mock_device_fqdn)
            device.ResetDelay()

    def _reset_dishes(self):
        """Reset Dish Devices"""
        for dish_master in self.dish_master_list:
            dish_master.SetDirectDishMode(DishMode.STANDBY_LP)
            dish_master.SetDirectState(DevState.STANDBY)
            dish_master.ResetDelay()

    def tear_down(self):
        """Tear down after each test run"""

        LOGGER.info("Calling Tear down for subarray")
        if self.obs_state in ("RESOURCING", "CONFIGURING", "SCANNING"):
            """Invoke Abort and Restart"""
            LOGGER.info("Invoking Abort on Subarray")
            self.abort_subarray()
            self.restart_subarray()
        elif self.obs_state == "ABORTED":
            """Invoke Restart"""
            LOGGER.info("Invoking Restart on Subarray")
            self.restart_subarray()
        else:
            self.force_change_of_obs_state("EMPTY")

        # Move Subarray to OFF state
        self.move_to_off()
        self._reset_dishes()
        self._reset_mock_devices()

    def clear_all_data(self):
        """Method to clear the observations
        and put the SubarrayNode in EMPTY"""
        if self.obs_state in [
            "IDLE",
            "RESOURCING",
            "READY",
            "CONFIGURING",
            "SCANNING",
        ]:
            self.abort_subarray()
            self.restart_subarray()

    def force_change_of_obs_state(self, dest_state_name):
        """Force SubarrayNode obsState to provided obsState

        Args:
            dest_state_name (str): Destination obsState
        """
        factory_obj = ObsStateResetterFactory()
        state_resetter = factory_obj.create_state_resetter(
            dest_state_name, self
        )
        state_resetter.reset()
