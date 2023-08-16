from ska_tango_base.control_model import HealthState
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
from tests.resources.test_harness.utils.sync_decorators import (
    sync_assign_resources,
)
from tests.resources.test_support.common_utils.common_helpers import Resource

device_dict = {
    "csp_master": csp_master,
    "tmc_subarraynode": tmc_subarraynode1,
    "sdp_master": sdp_master,
    "dish_master1": dish_master1,
    "dish_master2": dish_master2,
}


class CentralNode(object):
    """A TMC CentralNode class to implements the standard set
    of commands defined by the SKA Control Model.
    """

    def __init__(self) -> None:
        self.central_node = DeviceProxy(centralnode)
        self.subarray_devices = {
            "csp_subarray": csp_subarray1,
            "sdp_subarray": sdp_subarray1,
            "dish_master": dish_master1,
        }
        self.sdp_master = sdp_master
        self.csp_master = csp_master
        self.dish_master1 = dish_master1
        self.dish_master2 = dish_master2
        self.dish_master_list = [dish_master1, dish_master2]
        self._state = DevState.OFF

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

    def move_to_on(self):
        """
        A method to invoke TelescopeOn command to
        put telescope in ON state
        """
        # LOGGER.info(f"Invoking TelescopeOn on CentralNode")
        self.central_node.TelescopeOn()

        # TODO: where to keep this proxies ?
        device_to_on_list = [
            self.subarray_devices.get("csp_subarray"),
            self.subarray_devices.get("sdp_subarray"),
        ]
        for device in device_to_on_list:
            device_proxy = DeviceProxy(device)
            device_proxy.SetDirectState(DevState.ON)

        # If Dish master provided then set it to standby
        dish_master = self.subarray_devices.get("dish_master")
        device_proxy = DeviceProxy(dish_master)
        device_proxy.SetDirectState(DevState.STANDBY)

    def set_off(self):
        """
        A method to invoke TelescopeOff command to
        put telescope in OFF state

        """
        # LOGGER.info(f"Invoking TelescopeOff on CentralNode")
        self.central_node.TelescopeOff()

        # TODO: where to keep this proxies ?
        device_to_on_list = [
            self.subarray_devices.get("csp_subarray"),
            self.subarray_devices.get("sdp_subarray"),
        ]
        for device in device_to_on_list:
            device_proxy = DeviceProxy(device)
            device_proxy.SetDirectState(DevState.OFF)

        # If Dish master provided then set it to standby
        dish_master = self.subarray_devices.get("dish_master")
        device_proxy = DeviceProxy(dish_master)
        device_proxy.SetDirectState(DevState.STANDBY)

    def set_standby(self):
        """
        A method to invoke TelescopeStandby command to
        put telescope in STANDBY state

        """
        # LOGGER.info(f"Invoking TelescopeOff on CentralNode")
        self.central_node.TelescopeStandBy()

        # TODO: where to keep this proxies ?
        device_to_on_list = [
            self.subarray_devices.get("csp_subarray"),
            self.subarray_devices.get("sdp_subarray"),
        ]
        for device in device_to_on_list:
            device_proxy = DeviceProxy(device)
            device_proxy.SetDirectState(DevState.OFF)

        # If Dish master provided then set it to standby
        dish_master = self.subarray_devices.get("dish_master")
        device_proxy = DeviceProxy(dish_master)
        device_proxy.SetDirectState(DevState.STANDBY)

    @sync_assign_resources(device_dict=device_dict)
    def invoke_assign_resources(self, input_string):
        result, message = self.central_node.AssignResources(input_string)
        # LOGGER.info("Invoked AssignResources on CentralNode")
        return result, message

    def invoke_release_resources(self, input_string):
        result, message = self.central_node.ReleaseResources(input_string)
        # LOGGER.info("Invoked ReleaseResources on CentralNode")
        return result, message

    def _reset_health_state_for_mock_devices(self):
        """Reset Mock devices"""
        for mock_device in [
            self.sdp_master,
            self.csp_master,
            self.dish_master1,
            self.dish_master2,
        ]:
            device = DeviceProxy(mock_device)
            device.SetDirectHealthState(HealthState.UNKNOWN)

    def tear_down(self):
        """Handle Tear down of central Node"""
        # reset HealthState.UNKNOWN for mock devices
        self._reset_health_state_for_mock_devices()
