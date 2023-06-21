from tango import DeviceProxy, DevState
from tests.resources.test_support.helpers import resource
from tests.resources.test_harness.constant import centralnode, csp_subarray1, sdp_subarray1, dish_master1, tmc_subarraynode1
# from tests.conftest import LOGGER
# from tests.resources.test_support.sync_decorators import sync_assign_resources


class CentralNode(object):
    """ A TMC CentralNode class to implements the standard set
    of commands defined by the SKA Control Model.
    """
    def __init__(self) -> None:
        self.central_node = DeviceProxy(centralnode)
        self.subarray_node = tmc_subarraynode1
        self.subarray_devices = {"csp_subarray": csp_subarray1, "sdp_subarray": sdp_subarray1, "dish_master": dish_master1}
        self._state = DevState.OFF


    @property
    def state(self) -> DevState:
        """ TMC CentralNode operational state
        """
        self._state  = resource(self.central_node).get("State")
        return self._state 

    @state.setter
    def state(self, value):
        """Sets value for TMC CentralNode operational state

        Args:
            value (DevState): operational state value
        """
        self._state = value


    def set_on(self):
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


    def invoke_assign_resources(self, input_string):
        resource(self.subarray_node).assert_attribute("State").equals("ON")
        resource(self.subarray_node).assert_attribute("obsState").equals(
            "EMPTY"
        )
        result, message = self.central_node.AssignResources(input_string)
        # LOGGER.info("Invoked AssignResources on CentralNode")
        return result, message


    def invoke_release_resources(self, input_string):
        resource(self.subarray_node).assert_attribute("State").equals("ON")
        resource(self.subarray_node).assert_attribute("obsState").equals(
            "IDLE"
        )
        result, message = self.central_node.ReleaseResources(input_string)
        # LOGGER.info("Invoked ReleaseResources on CentralNode")
        return result, message
