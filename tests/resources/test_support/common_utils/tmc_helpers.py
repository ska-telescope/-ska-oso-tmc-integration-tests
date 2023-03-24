"""This module implement base helper class for tmc
"""
import logging
from tango import DeviceProxy, DevState
from tests.resources.test_support.common_utils.sync_decorators import sync_telescope_on, sync_set_to_off, sync_set_to_standby

LOGGER = logging.getLogger(__name__)

class TmcHelper(object):
    def __init__(self, central_node, **kwargs) -> None:
        self.devices = kwargs.get("device_list")
        self.tmc_devices = kwargs.get("tmc_devices")
        self.centralnode = central_node
    
    def check_devices(self):
        """
        """
        for device in self.devices:
            device_proxy = DeviceProxy(device)
            assert 0 < device_proxy.ping()
    
    @sync_telescope_on
    def set_to_on(self, device_list, **kwargs):
        central_node = DeviceProxy(self.centralnode)
        LOGGER.info(
            f"Before Sending TelescopeOn command {central_node} State is: {central_node.State()}"
        )
        central_node.TelescopeOn()
        for device in device_list:
            device_proxy = DeviceProxy(device)
            device_proxy.SetDirectState(DevState.ON)
            
    @sync_set_to_off
    def set_to_off(self, device_info, **kwargs):
        central_node = DeviceProxy(self.centralnode)
        central_node.TelescopeOff()
        for device in device_info:
            if type(device) is dict:
                device_name = device.get("name")
                state = device.get("state")
                device_proxy = DeviceProxy(device_name)
                device_proxy.SetDirectState(state)
            else:
                device_proxy = DeviceProxy(device)
                device_proxy.SetDirectState(DevState.OFF)
        LOGGER.info(
                f"After invoking TelescopeOff command {central_node} State is: {central_node.State()}"
        )
        
    @sync_set_to_standby
    def set_to_standby(self):
        central_node = DeviceProxy(self.centralnode)
        central_node.TelescopeStandBy()
        for device in self.tmc_devices:
            if type(device) is dict:
                device_name = device.get("name")
                state = device.get("state")
                device_proxy = DeviceProxy(device_name)
                device_proxy.SetDirectState(state)
            else:
                device_proxy.SetDirectState(DevState.OFF)
        LOGGER.info(
                f"After invoking TelescopeStandBy command {central_node} State is: {central_node.State()}"
        )

