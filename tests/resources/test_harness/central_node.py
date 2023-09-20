from ska_tango_base.control_model import HealthState
from tango import DeviceProxy, DevState

from tests.resources.test_harness.constant import (
    csp_master,
    device_dict,
    device_dict_low,
    dish_master1,
    dish_master2,
    low_csp_master,
    low_csp_master_leaf_node,
    low_sdp_master,
    low_sdp_master_leaf_node,
    sdp_master,
    tmc_csp_master_leaf_node,
    tmc_sdp_master_leaf_node,
)
from tests.resources.test_harness.utils.sync_decorators import (
    sync_assign_resources,
)
from tests.resources.test_support.common_utils.common_helpers import Resource


class CentralNode(object):
    """A TMC CentralNode class to implements the standard set
    of commands defined by the SKA Control Model.
    """

    def __init__(self, central_node) -> None:
        self.central_node = DeviceProxy(central_node)
        self.csp_master_leaf_node = None
        self.sdp_master_leaf_node = None
        self.sdp_master = None
        self.csp_master = None
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
        self.central_node.TelescopeOn()

        # device_to_on_list = [
        #     self.subarray_devices.get("csp_subarray"),
        #     self.subarray_devices.get("sdp_subarray"),
        # ]
        # for device in device_to_on_list:
        #     device_proxy = DeviceProxy(device)
        #     device_proxy.SetDirectState(DevState.ON)

        # # If Dish master provided then set it to standby
        # dish_master = self.subarray_devices.get("dish_master")
        # device_proxy = DeviceProxy(dish_master)
        # device_proxy.SetDirectState(DevState.STANDBY)

    def set_off(self):
        """
        A method to invoke TelescopeOff command to
        put telescope in OFF state

        """
        self.central_node.TelescopeOff()

        # device_to_on_list = [
        #     self.subarray_devices.get("csp_subarray"),
        #     self.subarray_devices.get("sdp_subarray"),
        # ]
        # for device in device_to_on_list:
        #     device_proxy = DeviceProxy(device)
        #     device_proxy.SetDirectState(DevState.OFF)

        # # If Dish master provided then set it to standby
        # dish_master = self.subarray_devices.get("dish_master")
        # device_proxy = DeviceProxy(dish_master)
        # device_proxy.SetDirectState(DevState.STANDBY)

    def set_standby(self):
        """
        A method to invoke TelescopeStandby command to
        put telescope in STANDBY state

        """
        self.central_node.TelescopeStandBy()

        # device_to_on_list = [
        #     self.subarray_devices.get("csp_subarray"),
        #     self.subarray_devices.get("sdp_subarray"),
        # ]
        # for device in device_to_on_list:
        #     device_proxy = DeviceProxy(device)
        #     device_proxy.SetDirectState(DevState.OFF)

        # # If Dish master provided then set it to standby
        # dish_master = self.subarray_devices.get("dish_master")
        # device_proxy = DeviceProxy(dish_master)
        # device_proxy.SetDirectState(DevState.STANDBY)

    @sync_assign_resources(device_dict=device_dict)
    def invoke_assign_resources(self, input_string):
        result, message = self.central_node.AssignResources(input_string)
        return result, message

    def invoke_release_resources(self, input_string):
        result, message = self.central_node.ReleaseResources(input_string)
        return result, message

    def _reset_health_state_for_mock_devices(self):
        """Reset Mock devices"""
        for mock_device in [self.sdp_master, self.csp_master]:
            device = DeviceProxy(mock_device)
            device.SetDirectHealthState(HealthState.UNKNOWN)

    def tear_down(self):
        """Handle Tear down of central Node"""
        # reset HealthState.UNKNOWN for mock devices
        self._reset_health_state_for_mock_devices()


class CentralNodeLow(CentralNode):
    """A TMC CentralNode class to implements the standard set
    of commands defined by the SKA Control Model for Low Telescope"""

    def __init__(self, central_node) -> None:
        super().__init__(central_node)
        self.csp_master_leaf_node = DeviceProxy(low_csp_master_leaf_node)
        self.sdp_master_leaf_node = DeviceProxy(low_sdp_master_leaf_node)
        # self.mccs_master_leaf_node = DeviceProxy(mccs_master_leaf_node)
        # self.subarray_devices = {
        #     "csp_subarray": low_csp_subarray1,
        #     "sdp_subarray": low_sdp_subarray1,
        #     "mccs_subarray": mccs_subarray1
        # }
        self.sdp_master = low_sdp_master
        self.csp_master = low_csp_master
        # self.mccs_master = mccs_controller
        self._state = DevState.OFF

    @sync_assign_resources(device_dict=device_dict_low)
    def invoke_assign_resources(self, input_string):
        result, message = self.central_node.AssignResources(input_string)
        return result, message

    # def _reset_health_state_for_mock_devices(self):
    #     """Reset Mock devices"""
    #     super()._reset_health_state_for_mock_devices()
    #     device = DeviceProxy(self.mccs_master)
    #     device.SetDirectHealthState(HealthState.UNKNOWN)


class CentralNodeMid(CentralNode):
    """A TMC CentralNode class to implements the standard set
    of commands defined by the SKA Control Model for Mid Telescope"""

    def __init__(self, central_node) -> None:
        super().__init__(central_node)
        self.csp_master_leaf_node = DeviceProxy(tmc_csp_master_leaf_node)
        self.sdp_master_leaf_node = DeviceProxy(tmc_sdp_master_leaf_node)
        # self.subarray_devices = {
        #     "csp_subarray": csp_subarray1,
        #     "sdp_subarray": sdp_subarray1,
        #     "dish_master": dish_master1,
        # }
        self.sdp_master = sdp_master
        self.csp_master = csp_master
        self.dish_master1 = dish_master1
        self.dish_master2 = dish_master2
        self.dish_master_list = [dish_master1, dish_master2]
        self._state = DevState.OFF

    def _reset_health_state_for_mock_devices(self):
        """Reset Mock devices"""
        super()._reset_health_state_for_mock_devices()
        for mock_device in [
            self.dish_master1,
            self.dish_master2,
        ]:
            device = DeviceProxy(mock_device)
            device.SetDirectHealthState(HealthState.UNKNOWN)


# csp_subarray1, low_csp_subarray1, low_sdp_subarray1, mccs_controller,
# mccs_subarray1,sdp_subarray1, tmc_low_subarraynode1, tmc_subarraynode1,
