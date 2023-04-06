"""This module implement base helper class for tmc
"""
import logging
from tango import DeviceProxy, DevState
from tests.resources.test_support.common_utils.sync_decorators import (
    sync_telescope_on, sync_set_to_off, sync_set_to_standby,sync_release_resources,
    sync_assign_resources,sync_abort,sync_restart,sync_configure,sync_end
)
from tests.resources.test_support.common_utils.common_helpers import  resource
LOGGER = logging.getLogger(__name__)

class TmcHelper(object):
    def __init__(self, central_node, **kwargs) -> None:
        """
        Args:
            central_node (str) -> FQDN of Central Node
        """
        self.centralnode = central_node
    
    def check_devices(self, device_list: list) -> None:
        """
        Args:
            device_list (list): List of devices to check if it is ON.
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


    @sync_set_to_standby
    def set_to_standby(self, **kwargs):
        central_node = DeviceProxy(self.centralnode)
        central_node.TelescopeStandBy()
        device_to_standby_list = [kwargs.get("csp_subarray"), kwargs.get("sdp_subarray")]
        for device in device_to_standby_list:
            device_proxy = DeviceProxy(device)
            device_proxy.SetDirectState(DevState.OFF)

        LOGGER.info(
            f"After invoking TelescopeStandBy command {central_node} State is: {central_node.State()}"
        )


    @sync_release_resources
    def invoke_releaseResources(self, release_input_str,**kwargs,):
        central_node = DeviceProxy(self.centralnode)
        central_node.ReleaseResources(release_input_str)
        LOGGER.info(
            f"ReleaseResources command is invoked on {central_node}"
        )
        device_to_standby_list = [kwargs.get("csp_subarray"), kwargs.get("sdp_subarray")]
        for device in device_to_standby_list:
            device_proxy = DeviceProxy(device)
            device_proxy.SetDirectState(DevState.OFF)


    @sync_assign_resources()
    def compose_sub(self,assign_res_input,**kwargs):
        resource(kwargs.get("tmc_subarraynode")).assert_attribute("State").equals(
            "ON"
        )
        resource(kwargs.get("tmc_subarraynode")).assert_attribute("obsState").equals(
            "EMPTY"
        )
        central_node = DeviceProxy(self.centralnode)
        central_node.AssignResources(assign_res_input)
        LOGGER.info("Invoked AssignResources on CentralNode")

    
    @sync_configure()
    def configure_subarray(self,configure_input_str,**kwargs):
        resource(kwargs.get("tmc_subarraynode")).assert_attribute("obsState").equals(
            "IDLE"
        )
        subarray_node = DeviceProxy(kwargs.get("tmc_subarraynode"))
        subarray_node.Configure(configure_input_str)
        LOGGER.info("Invoked Configure on SubarrayNode")

    @sync_end()
    def end(**kwargs):
        subarray_node = DeviceProxy(kwargs.get("tmc_subarraynode"))
        subarray_node.End()
        LOGGER.info(
            f"End command is invoked on {subarray_node}"
        )

    # @sync_scan()
    # def scan(scan_input):
    #     resource(tmc_subarraynode1).assert_attribute("obsState").equals(
    #         "READY"
    #     )
    #     subarray_node = DeviceProxy(tmc_subarraynode1)
    #     subarray_node.Scan(scan_input)
    #     LOGGER.info("Invoked Scan on SubarrayNode")


    @sync_abort()
    def invoke_abort(self,**kwargs):
        subarray_node = DeviceProxy(kwargs.get("tmc_subarraynode"))
        subarray_node.Abort()
        LOGGER.info("Invoked Abort on SubarrayNode")


    @sync_restart()
    def invoke_restart(self,**kwargs):
        subarray_node = DeviceProxy(kwargs.get("tmc_subarraynode"))
        subarray_node.Restart()
        LOGGER.info("Invoked Restart on SubarrayNode")


    # def set_device_obsstate_configuring():
    #     csp_subarray = DeviceProxy(csp_subarray1)
    #     csp_subarray.SetDirectObsState(ObsState.CONFIGURING)
    #     sdp_subarray = DeviceProxy(sdp_subarray1)
    #     sdp_subarray.SetDirectObsState(ObsState.CONFIGURING)

    # def set_device_obsstate_resourcing():
    #     csp_subarray = DeviceProxy(csp_subarray1)
    #     csp_subarray.SetDirectObsState(ObsState.RESOURCING)
    #     sdp_subarray = DeviceProxy(sdp_subarray1)
    #     sdp_subarray.SetDirectObsState(ObsState.RESOURCING)
