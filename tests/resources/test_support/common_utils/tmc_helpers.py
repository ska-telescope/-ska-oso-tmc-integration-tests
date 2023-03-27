"""This module implement base helper class for tmc
"""
import logging
from tango import DeviceProxy, DevState
from tests.resources.test_support.common_utils.sync_decorators import sync_telescope_on, sync_set_to_off, sync_set_to_standby

LOGGER = logging.getLogger(__name__)

class TmcHelper(object):
    def __init__(self, central_node, **kwargs) -> None:
        """
        Args:
            central_node (str) -> Name of Central Node 
        """
        self.centralnode = central_node
    
    def check_devices(self, device_list):
        """
        """
        for device in device_list:
            device_proxy = DeviceProxy(device)
            assert 0 < device_proxy.ping()
    
    @sync_telescope_on
    def set_to_on(self, **kwargs) -> None:
        """
        Args:
            kwargs (dict): device info which needs set to ON
        """
        central_node = DeviceProxy(self.centralnode)
        LOGGER.info(
            f"Before Sending TelescopeOn command {central_node} State is: {central_node.State()}"
        )
        central_node.TelescopeOn()
        device_to_on_list = [kwargs.get("csp_subarray"), kwargs.get("sdp_subarray"), kwargs.get("dish_master")]
        for device in device_to_on_list:
            if device:
                device_proxy = DeviceProxy(device)
                device_proxy.SetDirectState(DevState.ON)
            
    @sync_set_to_off
    def set_to_off(self, **kwargs):
        central_node = DeviceProxy(self.centralnode)
        central_node.TelescopeOff()
        device_to_off_list = [kwargs.get("csp_subarray"), kwargs.get("sdp_subarray")]
        for device in device_to_off_list:
            device_proxy = DeviceProxy(device)
            device_proxy.SetDirectState(DevState.OFF)
        
        # If Dish master provided then set it to standby
        dish_master = kwargs.get("dish_master")
        if dish_master:
            device_proxy = DeviceProxy(dish_master)
            device_proxy.SetDirectState(DevState.STANDBY)
        
        LOGGER.info(
                f"After invoking TelescopeOff command {central_node} State is: {central_node.State()}"
        )


