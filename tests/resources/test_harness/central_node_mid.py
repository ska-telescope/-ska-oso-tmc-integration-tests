import logging
import os

from ska_control_model import ObsState
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
    dish_master3,
    sdp_master,
    sdp_subarray1,
    tmc_csp_master_leaf_node,
    tmc_sdp_master_leaf_node,
    tmc_subarraynode1,
)
from tests.resources.test_harness.helpers import (
    SIMULATED_DEVICES_DICT,
    wait_csp_master_off,
)
from tests.resources.test_harness.utils.common_utils import JsonFactory
from tests.resources.test_harness.utils.enums import DishMode
from tests.resources.test_harness.utils.sync_decorators import sync_set_to_off
from tests.resources.test_harness.utils.wait_helpers import Waiter

configure_logging(logging.DEBUG)
LOGGER = logging.getLogger(__name__)

REAL_DISH1_FQDN = os.getenv("DISH_NAME_1")
REAL_DISH36_FQDN = os.getenv("DISH_NAME_36")
REAL_DISH63_FQDN = os.getenv("DISH_NAME_63")


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

        if (
            SIMULATED_DEVICES_DICT["csp_and_sdp"]
            and not SIMULATED_DEVICES_DICT["all_mocks"]
        ):
            dish_fqdn1 = REAL_DISH1_FQDN
            dish_fqdn36 = REAL_DISH36_FQDN
            dish_fqdn63 = REAL_DISH63_FQDN
        else:
            dish_fqdn1 = dish_master1
            dish_fqdn36 = dish_master2
            dish_fqdn63 = dish_master3

        self.dish_master_list = [
            DeviceProxy(dish_fqdn1),
            DeviceProxy(dish_fqdn36),
            DeviceProxy(dish_fqdn63),
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

    def set_subarray_id(self, requested_subarray_id: str) -> None:
        """This method creates subarray devices for the requested subarray
        id"""
        self.subarray_node = DeviceProxy(
            f"ska_mid/tm_subarray_node/{requested_subarray_id}"
        )
        subarray_id = str(requested_subarray_id).zfill(2)
        self.subarray_devices = {
            "csp_subarray": DeviceProxy(f"mid-csp/subarray/{subarray_id}"),
            "sdp_subarray": DeviceProxy(f"mid-sdp/subarray/{subarray_id}"),
        }
        self.csp_subarray_leaf_node = DeviceProxy(
            f"ska_mid/tm_leaf_node/csp_subarray{subarray_id}"
        )
        self.sdp_subarray_leaf_node = DeviceProxy(
            f"ska_mid/tm_leaf_node/sdp_subarray{subarray_id}"
        )

    def _reset_health_state_for_mock_devices(self):
        """Reset Mock devices"""
        super()._reset_health_state_for_mock_devices()
        if (
            SIMULATED_DEVICES_DICT["sdp_and_dish"]
            or SIMULATED_DEVICES_DICT["csp_and_dish"]
            or SIMULATED_DEVICES_DICT["all_mocks"]
        ):
            for mock_device in self.dish_master_list:
                mock_device.SetDirectHealthState(HealthState.UNKNOWN)

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
            SIMULATED_DEVICES_DICT["csp_and_dish"]
            or SIMULATED_DEVICES_DICT["all_mocks"]
        ):
            for mock_device in self.dish_master_list:
                mock_device.SetKValue(0)

        if (
            SIMULATED_DEVICES_DICT["csp_and_dish"]
            or SIMULATED_DEVICES_DICT["all_mocks"]
        ):
            self.csp_master.ResetSysParams()

    def _clear_command_call_and_transition_data(self, clear_transition=False):
        """Clears the command call data"""
        if SIMULATED_DEVICES_DICT["all_mocks"]:
            for sim_device in [
                csp_subarray1,
                sdp_subarray1,
                dish_master1,
                dish_master2,
                dish_master3,
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
            if self.csp_master.adminMode != 0:
                self.csp_master.adminMode = 0
            wait_csp_master_off()
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
        if SIMULATED_DEVICES_DICT["all_mocks"]:
            LOGGER.info("Invoking TelescopeOff() with all Mocks")
            self.central_node.TelescopeOff()
            self.set_subarraystate_and_dishmode_with_all_mocks(
                DevState.OFF, DishMode.STANDBY_LP
            )

        elif SIMULATED_DEVICES_DICT["csp_and_sdp"]:
            LOGGER.info("Invoking TelescopeOff() on simulated csp and sdp")
            self.central_node.TelescopeOff()
            self.set_value_with_csp_sdp_mocks(DevState.OFF)

        elif SIMULATED_DEVICES_DICT["csp_and_dish"]:
            LOGGER.info("Invoking TelescopeOff() on simulated csp and Dish")
            self.central_node.TelescopeOff()
            self.set_values_with_csp_dish_mocks(
                DevState.OFF, DishMode.STANDBY_LP
            )

        elif SIMULATED_DEVICES_DICT["sdp_and_dish"]:
            LOGGER.info("Invoking TelescopeOff() on simulated sdp and dish")
            self.central_node.TelescopeOff()
            self.set_values_with_sdp_dish_mocks(
                DevState.OFF, DishMode.STANDBY_LP
            )
        else:
            LOGGER.info("Invoke TelescopeOff() with all real sub-systems")
            self.central_node.TelescopeOff()

    def tear_down(self):
        """Handle Tear down of central Node"""
        Subarray_node_obsstate = self.subarray_node.obsState
        LOGGER.info(
            f"Calling tear down for CentralNode for SubarrayNode's \
                {Subarray_node_obsstate} obsstate."
        )
        # reset HealthState.UNKNOWN for mock devices
        self._reset_health_state_for_mock_devices()
        self._reset_sys_param_and_k_value()
        if self.subarray_node.obsState == ObsState.IDLE:
            LOGGER.info("Calling Release Resource on centralnode")
            self.invoke_release_resources(self.release_input)
        elif self.subarray_node.obsState in [
            ObsState.RESOURCING,
            ObsState.SCANNING,
            ObsState.CONFIGURING,
            ObsState.READY,
            ObsState.IDLE,
        ]:
            LOGGER.info("Calling Abort and Restart on SubarrayNode")
            self.subarray_abort()
            self.subarray_restart()
        elif self.subarray_node.obsState == ObsState.ABORTED:
            self.subarray_restart()
        self.move_to_off()
        self._clear_command_call_and_transition_data(clear_transition=True)
