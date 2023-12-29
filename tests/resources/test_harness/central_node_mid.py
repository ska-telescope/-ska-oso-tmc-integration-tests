import json
import logging
import os
from typing import Tuple

from ska_control_model import ObsState, ResultCode
from ska_ser_logging import configure_logging
from ska_tango_base.control_model import HealthState
from tango import DeviceProxy, DevState

from tests.resources.test_harness.central_node import CentralNodeWrapper
from tests.resources.test_harness.constant import (
    centralnode,
    csp_master,
    csp_subarray1,
    device_dict,
    dish_master1,
    dish_master2,
    sdp_master,
    sdp_subarray1,
    tmc_csp_master_leaf_node,
    tmc_sdp_master_leaf_node,
    tmc_subarraynode1,
)
from tests.resources.test_harness.helpers import generate_eb_pb_ids
from tests.resources.test_harness.utils.common_utils import JsonFactory
from tests.resources.test_harness.utils.enums import DishMode
from tests.resources.test_harness.utils.sync_decorators import (
    sync_abort,
    sync_assign_resources,
    sync_release_resources,
    sync_restart,
    sync_set_to_off,
)
from tests.resources.test_harness.utils.wait_helpers import Waiter

configure_logging(logging.DEBUG)
LOGGER = logging.getLogger(__name__)

SDP_SIMULATION_ENABLED = os.getenv("SDP_SIMULATION_ENABLED")
CSP_SIMULATION_ENABLED = os.getenv("CSP_SIMULATION_ENABLED")
DISH_SIMULATION_ENABLED = os.getenv("DISH_SIMULATION_ENABLED")
REAL_DISH1_FQDN = os.getenv("DISH_NAME_1")
REAL_DISH2_FQDN = os.getenv("DISH_NAME_2")


class CentralNodeWrapperMid(CentralNodeWrapper):
    """A wrapper class to implement common tango specific details
    and standard set of commands for TMC Mid CentralNode,
    defined by the SKA Control Model."""

    def __init__(self) -> None:
        super().__init__()
        self.central_node = DeviceProxy(centralnode)
        self.subarray_node = DeviceProxy(tmc_subarraynode1)
        self.csp_master_leaf_node = DeviceProxy(tmc_csp_master_leaf_node)
        self.sdp_master_leaf_node = DeviceProxy(tmc_sdp_master_leaf_node)
        self.sdp_master = DeviceProxy(sdp_master)
        self.subarray_devices = {
            "csp_subarray": DeviceProxy(csp_subarray1),
            "sdp_subarray": DeviceProxy(sdp_subarray1),
        }

        self.csp_master = DeviceProxy(csp_master)
        self.simulated_devices_dict = self.get_simulated_devices_info()
        if (
            self.simulated_devices_dict["csp_and_sdp"]
            and not self.simulated_devices_dict["all_mocks"]
        ):
            dish_fqdn1 = REAL_DISH1_FQDN
            dish_fqdn2 = REAL_DISH2_FQDN
        else:
            dish_fqdn1 = dish_master1
            dish_fqdn2 = dish_master2

        self.dish_master_list = [
            DeviceProxy(dish_fqdn1),
            DeviceProxy(dish_fqdn2),
        ]

        self._state = DevState.OFF
        self.json_factory = JsonFactory()
        self.release_input = (
            self.json_factory.create_centralnode_configuration(
                "release_resources_mid"
            )
        )
        device_dict["cbf_subarray1"] = "mid_csp_cbf/sub_elt/subarray_01"
        device_dict["cbf_controller"] = "mid_csp_cbf/sub_elt/controller"
        self.wait = Waiter(**device_dict)
        self.simulated_devices_dict = self.get_simulated_devices_info()

    def load_dish_vcc_configuration(self, dish_vcc_config: str):
        """Invoke LoadDishCfg command on central Node
        :param dish_vcc_config: Dish vcc configuration json string
        """
        result, message = self.central_node.LoadDishCfg(dish_vcc_config)
        return result, message

    def _reset_sys_param_and_k_value(self):
        """Reset sysParam and sourceSysParam attribute of csp master
        reset kValue of Dish master
        """
        if (
            self.simulated_devices_dict["csp_and_dish"]
            or self.simulated_devices_dict["all_mocks"]
        ):
            for mock_device in self.dish_master_list:
                mock_device.SetKValue(0)

        if (
            self.simulated_devices_dict["csp_and_dish"]
            or self.simulated_devices_dict["all_mocks"]
        ):

            self.csp_master.ResetSysParams()

    def _clear_command_call_and_transition_data(self, clear_transition=False):
        """Clears the command call data"""
        if self.simulated_devices_dict["all_mocks"]:
            for sim_device in [
                csp_subarray1,
                sdp_subarray1,
                dish_master1,
                dish_master2,
            ]:
                device = DeviceProxy(sim_device)
                device.ClearCommandCallInfo()
                if clear_transition:
                    device.ResetTransitions()

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

    @sync_set_to_off(device_dict=device_dict)
    def move_to_off(self):
        """
        A method to invoke TelescopeOff command to
        put telescope in OFF state

        """
        if self.simulated_devices_dict["all_mocks"]:
            LOGGER.info("Invoking TelescopeOff() with all Mocks")
            self.central_node.TelescopeOff()
            self.set_subarraystate_and_dishmode_with_all_mocks(
                DevState.OFF, DishMode.STANDBY_LP
            )

        elif self.simulated_devices_dict["csp_and_sdp"]:
            LOGGER.info("Invoking TelescopeOff() on simulated csp and sdp")
            self.central_node.TelescopeOff()
            self.set_value_with_csp_sdp_mocks(DevState.OFF)

        elif self.simulated_devices_dict["csp_and_dish"]:
            LOGGER.info("Invoking TelescopeOff() on simulated csp and Dish")
            self.central_node.TelescopeOff()
            self.set_values_with_csp_dish_mocks(
                DevState.OFF, DishMode.STANDBY_LP
            )

        elif self.simulated_devices_dict["sdp_and_dish"]:
            LOGGER.info("Invoking TelescopeOff() on simulated sdp and dish")
            self.central_node.TelescopeOff()
            self.set_values_with_sdp_dish_mocks(
                DevState.OFF, DishMode.STANDBY_LP
            )

        else:
            LOGGER.info("Invoke TelescopeOff() with all real sub-systems")
            self.central_node.TelescopeOff()

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

    @sync_assign_resources(device_dict=device_dict)
    def store_resources(self, assign_json: str):
        """Invoke Assign Resource command on central Node
        Args:
            assign_json (str): Assign resource input json
        """
        input_json = json.loads(assign_json)
        generate_eb_pb_ids(input_json)
        result, message = self.central_node.AssignResources(
            json.dumps(input_json)
        )
        LOGGER.info("Invoked AssignResources on CentralNode")
        return result, message

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
        if self.simulated_devices_dict["csp_and_sdp"]:
            for mock_device in [
                self.sdp_master,
                self.csp_master,
            ]:
                device = DeviceProxy(mock_device)
                device.SetDirectHealthState(HealthState.UNKNOWN)
        elif self.simulated_devices_dict["csp_and_dish"]:
            self.csp_master.SetDirectHealthState(HealthState.UNKNOWN)
            for mock_device in self.dish_master_list:
                mock_device.SetDirectHealthState(HealthState.UNKNOWN)
        elif self.simulated_devices_dict["sdp_and_dish"]:
            self.sdp_master.SetDirectHealthState(HealthState.UNKNOWN)
            for mock_device in self.dish_master_list:
                mock_device.SetDirectHealthState(HealthState.UNKNOWN)
        elif self.simulated_devices_dict["all_mocks"]:
            for mock_device in [
                self.sdp_master,
                self.csp_master,
            ]:
                device = DeviceProxy(mock_device)
                device.SetDirectHealthState(HealthState.UNKNOWN)
            for mock_device in self.dish_master_list:
                mock_device.SetDirectHealthState(HealthState.UNKNOWN)
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

    def tear_down(self):
        """Handle Tear down of central Node"""
        LOGGER.info("Calling Tear down for Central node.")
        # reset HealthState.UNKNOWN for mock devices
        self._reset_health_state_for_mock_devices()
        self._reset_sys_param_and_k_value()
        if self.subarray_node.obsState == ObsState.IDLE:
            LOGGER.info("Calling Release Resource on centralnode")
            self.invoke_release_resources(self.release_input)
        elif self.subarray_node.obsState == ObsState.RESOURCING:
            LOGGER.info("Calling Abort and Restart on SubarrayNode")
            self.subarray_abort()
            self.subarray_restart()
        elif self.subarray_node.obsState == ObsState.ABORTED:
            self.subarray_restart()
        self.move_to_off()
        self._clear_command_call_and_transition_data(clear_transition=True)
