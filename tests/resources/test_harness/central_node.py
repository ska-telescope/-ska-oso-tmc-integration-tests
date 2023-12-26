import logging
import os
from typing import Tuple

from ska_control_model import ResultCode
from ska_tango_base.control_model import HealthState
from tango import DeviceProxy, DevState

from tests.resources.test_harness.constant import device_dict
from tests.resources.test_harness.utils.enums import DishMode
from tests.resources.test_harness.utils.sync_decorators import (
    sync_abort,
    sync_release_resources,
    sync_restart,
)
from tests.resources.test_support.common_utils.common_helpers import Resource

LOGGER = logging.getLogger(__name__)


SDP_SIMULATION_ENABLED = os.getenv("SDP_SIMULATION_ENABLED")
CSP_SIMULATION_ENABLED = os.getenv("CSP_SIMULATION_ENABLED")
DISH_SIMULATION_ENABLED = os.getenv("DISH_SIMULATION_ENABLED")


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
        self.simulated_devices_dict = self.get_simulated_devices_info()

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

    def move_to_on(self):
        """
        A method to invoke TelescopeOn command to
        put telescope in ON state
        """
        LOGGER.info("Starting up the Telescope")
        LOGGER.info(
            f"Received simulated devices: {self.simulated_devices_dict}"
        )
        if self.simulated_devices_dict["all_mocks"]:
            LOGGER.info("Invoking TelescopeOn() with all Mocks")
            self.central_node.TelescopeOn()
            self.set_subarraystate_and_dishmode_with_all_mocks(
                DevState.ON, DishMode.STANDBY_FP
            )

        elif self.simulated_devices_dict["csp_and_sdp"]:
            LOGGER.info("Invoking TelescopeOn() on simulated csp and sdp")
            self.central_node.TelescopeOn()
            self.set_value_with_csp_sdp_mocks(DevState.ON)

        elif self.simulated_devices_dict["csp_and_dish"]:
            LOGGER.info("Invoking TelescopeOn() on simulated csp and Dish")
            self.central_node.TelescopeOn()
            self.set_values_with_csp_dish_mocks(
                DevState.ON, DishMode.STANDBY_FP
            )

        elif self.simulated_devices_dict["sdp_and_dish"]:
            LOGGER.info("Invoking TelescopeOn() on simulated sdp and dish")
            self.central_node.TelescopeOn()
            self.set_values_with_sdp_dish_mocks(
                DevState.ON, DishMode.STANDBY_FP
            )
        else:
            LOGGER.info("Invoke TelescopeOn() on all real sub-systems")
            self.central_node.TelescopeOn()

    def set_standby(self):
        """
        A method to invoke TelescopeStandby command to
        put telescope in STANDBY state

        """
        LOGGER.info("Putting Telescope in Standby state")
        if self.simulated_devices_dict["all_mocks"]:
            LOGGER.info("Invoking TelescopeStandBy() with all Mocks")
            self.central_node.TelescopeStandBy()
            self.set_subarraystate_and_dishmode_with_all_mocks(
                DevState.STANDBY, DevState.STANDBY
            )

        elif self.simulated_devices_dict["csp_and_sdp"]:
            LOGGER.info("Invoking TelescopeStandBy() on simulated csp and sdp")
            self.central_node.TelescopeStandBy()
            self.set_value_with_csp_sdp_mocks(DevState.STANDBY)

        elif self.simulated_devices_dict["csp_and_dish"]:
            LOGGER.info(
                "Invoking TelescopeStandBy() on simulated csp and Dish"
            )
            self.central_node.TelescopeStandBy()
            self.set_values_with_csp_dish_mocks(
                DevState.STANDBY, DevState.STANDBY
            )

        elif self.simulated_devices_dict["sdp_and_dish"]:
            LOGGER.info(
                "Invoking TelescopeStandBy() on simulated sdp and dish"
            )
            self.central_node.TelescopeStandBy()
            self.set_values_with_sdp_dish_mocks(
                DevState.STANDBY, DevState.STANDBY
            )
        else:
            LOGGER.info("Invoke TelescopeStandBy() with all real sub-systems")
            self.central_node.TelescopeStandBy()

    @sync_release_resources(device_dict=device_dict)
    def invoke_release_resources(self, input_string):
        """Invoke Release Resource command on central Node
        Args:
            input_string (str): Release resource input json
        """
        result, message = self.central_node.ReleaseResources(input_string)
        return result, message

    @sync_abort(device_dict=device_dict)
    def subarray_abort(self):
        """Invoke Abort command on subarray Node"""
        result, message = self.subarray_node.Abort()
        return result, message

    @sync_restart(device_dict=device_dict)
    def subarray_restart(self):
        """Invoke Restart command on subarray Node"""
        result, message = self.subarray_node.Restart()
        return result, message

    def _reset_health_state_for_mock_devices(self):
        """Reset Mock devices"""
        if (
            self.simulated_devices_dict["csp_and_sdp"]
            or self.simulated_devices_dict["all_mocks"]
        ):
            for mock_device in [
                self.sdp_master,
                self.csp_master,
            ]:
                device = DeviceProxy(mock_device)
                device.SetDirectHealthState(HealthState.UNKNOWN)
        elif self.simulated_devices_dict["csp_and_dish"]:
            for mock_device in [
                self.csp_master,
            ]:
                device = DeviceProxy(mock_device)
                device.SetDirectHealthState(HealthState.UNKNOWN)
        elif self.simulated_devices_dict["sdp_and_dish"]:
            for mock_device in [
                self.sdp_master,
            ]:
                device = DeviceProxy(mock_device)
                device.SetDirectHealthState(HealthState.UNKNOWN)
        else:
            LOGGER.info("No devices to reset healthState")

    def perform_action(
        self, command_name: str, input_json: str
    ) -> Tuple[ResultCode, str]:
        """Execute provided command on centralnode
        Args:
            command_name (str): Name of command to execute
            input_json (str): Json send as input to execute command
        """

        result, message = self.central_node.command_inout(
            command_name, input_json
        )
        return result, message

    def set_subarraystate_and_dishmode_with_all_mocks(
        self, subarray_state, dish_mode
    ):
        """
        A method to set values on mock CSP, SDP and Dish devices.
        Args:
            subarray_state: DevState - subarray state value for
                                        CSP and SDP Subarrays
            dish_mode: DishMode - dish mode value for Dish Masters
        """
        device_to_on_list = [
            self.subarray_devices.get("csp_subarray"),
            self.subarray_devices.get("sdp_subarray"),
        ]
        for device in device_to_on_list:
            device_proxy = DeviceProxy(device)
            device_proxy.SetDirectState(subarray_state)

        # If Dish master provided then set it to standby
        if self.dish_master_list:
            for device in self.dish_master_list:
                device.SetDirectDishMode(dish_mode)

    def set_value_with_csp_sdp_mocks(self, subarray_state):
        """
        A method to set values on mock CSP and SDP devices.
        Args:
            subarray_state: DevState - subarray state value for
                                    CSP and SDP Subarrays
        """
        device_to_on_list = [
            self.subarray_devices.get("csp_subarray"),
            self.subarray_devices.get("sdp_subarray"),
        ]
        for device in device_to_on_list:
            device_proxy = DeviceProxy(device)
            device_proxy.SetDirectState(subarray_state)

    def set_values_with_csp_dish_mocks(self, subarray_state, dish_mode):
        """
        A method to set values on mock CSP and Dish devices.
        Args:
            subarray_state: DevState - subarray state value for
                                    CSP Subarray
            dish_mode: DishMode - dish mode value for Dish Masters
        """
        device_to_on_list = [
            self.subarray_devices.get("csp_subarray"),
        ]
        for device in device_to_on_list:
            device_proxy = DeviceProxy(device)
            device_proxy.SetDirectState(subarray_state)

        # If Dish master provided then set it to standby
        if self.dish_master_list:
            for device in self.dish_master_list:
                device.SetDirectDishMode(dish_mode)

    def set_values_with_sdp_dish_mocks(self, subarray_state, dish_mode):
        """
        A method to set values on mock SDP and Dish devices.
        Args:
            subarray_state: DevState - subarray state value for
                                    SDP Subarray
            dish_mode: DishMode - dish mode value for Dish Masters
        """
        device_to_on_list = [self.subarray_devices.get("sdp_subarray")]
        for device in device_to_on_list:
            device_proxy = DeviceProxy(device)
            device_proxy.SetDirectState(subarray_state)

        # If Dish master provided then set it to standby
        if self.dish_master_list:
            for device in self.dish_master_list:
                device.SetDirectDishMode(dish_mode)

    def get_simulated_devices_info(self) -> dict:
        """
        A method to get simulated devices present in the deployement.

        return: dict
        """
        self.is_csp_simulated = CSP_SIMULATION_ENABLED.lower() == "true"
        self.is_sdp_simulated = SDP_SIMULATION_ENABLED.lower() == "true"
        self.is_dish_simulated = DISH_SIMULATION_ENABLED.lower() == "true"
        return {
            "csp_and_sdp": all(
                [self.is_csp_simulated, self.is_sdp_simulated]
            ),  # real DISH.LMC enabled
            "csp_and_dish": all(
                [self.is_csp_simulated, self.is_dish_simulated]
            ),  # real SDP enabled
            "sdp_and_dish": all(
                [self.is_sdp_simulated, self.is_dish_simulated]
            ),  # real CSP.LMC enabled
            "all_mocks": all(
                [
                    self.is_csp_simulated,
                    self.is_sdp_simulated,
                    self.is_dish_simulated,
                ]
            ),
        }
