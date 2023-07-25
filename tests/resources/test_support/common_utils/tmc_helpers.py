"""This module implement base helper class for tmc
"""
import logging
import re
from typing import Optional

from tango import DeviceProxy, DevState

from tests.resources.test_support.common_utils.common_helpers import resource
from tests.resources.test_support.common_utils.sync_decorators import (
    sync_abort,
    sync_assign_resources,
    sync_assigning,
    sync_configure,
    sync_configure_sub,
    sync_end,
    sync_endscan,
    sync_endscan_in_ready,
    sync_release_resources,
    sync_restart,
    sync_scan,
    sync_set_to_off,
    sync_set_to_standby,
    sync_telescope_on,
)
from tests.resources.test_support.common_utils.telescope_controls import (
    BaseTelescopeControl,
)
from tests.resources.test_support.constant import (
    DEVICE_OBS_STATE_ABORT_INFO,
    DEVICE_OBS_STATE_EMPTY_INFO,
    DEVICE_OBS_STATE_IDLE_INFO,
    DEVICE_STATE_STANDBY_INFO,
    ON_OFF_DEVICE_COMMAND_DICT,
)

resutl, message = "", ""
LOGGER = logging.getLogger(__name__)


class TmcHelper(object):
    """TmcHelper class"""

    def __init__(self, central_node, subarray_node, **kwargs) -> None:
        """
        Args:
            central_node (str) -> FQDN of Central Node
        """
        self.centralnode = central_node
        self.subarray_node = subarray_node

    def check_devices(self, device_list: list) -> None:
        """
        Args:
            device_list (list): List of devices to check if it is ON.
        """
        for device in device_list:
            device_proxy = DeviceProxy(device)
            assert 0 < device_proxy.ping()

    def check_telescope_availability(self) -> None:
        """
        Checks of Telescope availability is set to True
        CSP , SDP Master should be True
        At least one of the Subarray node should be available
        """
        # Check if at least 1 subarry node is true

        central_node = DeviceProxy(self.centralnode)
        telescopeavailability = central_node.read_attribute(
            "telescopeAvailability"
        ).value
        nodes = re.findall(
            r"tmc_subarrays\": {(.*?)}", telescopeavailability, re.DOTALL
        )
        assert "true" in re.findall(r": (\w*)", nodes[0], re.DOTALL)

        # Check if CSP/SDP master nodes are true in telescopeavailability
        assert "true" in re.findall(
            r"csp_master_leaf_node\": (.*),", telescopeavailability, re.DOTALL
        )
        assert "true" in re.findall(
            r"sdp_master_leaf_node\": (.*)}", telescopeavailability, re.DOTALL
        )

    @sync_telescope_on
    def set_to_on(self, **kwargs) -> None:
        """
        Args:
            kwargs (dict): device info which needs set to ON
        """

        central_node = DeviceProxy(self.centralnode)
        LOGGER.info(
            f"Before Sending TelescopeOn command {central_node}\
            State is:{central_node.State()}"
        )
        central_node.TelescopeOn()
        device_to_on_list = [
            kwargs.get("csp_subarray"),
            kwargs.get("sdp_subarray"),
        ]
        for device in device_to_on_list:
            if device:
                device_proxy = DeviceProxy(device)
                device_proxy.SetDirectState(DevState.ON)

        # If Dish master provided then set it to standby
        dish_master = kwargs.get("dish_master")
        if dish_master:
            device_proxy = DeviceProxy(dish_master)
            device_proxy.SetDirectState(DevState.STANDBY)

    @sync_set_to_off
    def set_to_off(self, **kwargs):
        central_node = DeviceProxy(self.centralnode)
        central_node.TelescopeOff()
        device_to_off_list = [
            kwargs.get("csp_subarray"),
            kwargs.get("sdp_subarray"),
        ]
        for device in device_to_off_list:
            device_proxy = DeviceProxy(device)
            device_proxy.SetDirectState(DevState.OFF)

        # If Dish master provided then set it to standby
        dish_master = kwargs.get("dish_master")
        if dish_master:
            device_proxy = DeviceProxy(dish_master)
            device_proxy.SetDirectState(DevState.STANDBY)

        LOGGER.info(
            f"After invoking TelescopeOff command {central_node} State is:\
            {central_node.State()}"
        )

    @sync_set_to_standby
    def set_to_standby(self, **kwargs):
        central_node = DeviceProxy(self.centralnode)
        central_node.TelescopeStandBy()
        device_to_standby_list = [
            kwargs.get("csp_subarray"),
            kwargs.get("sdp_subarray"),
        ]
        for device in device_to_standby_list:
            device_proxy = DeviceProxy(device)
            device_proxy.SetDirectState(DevState.OFF)

        # If Dish master provided then set it to standby
        dish_master = kwargs.get("dish_master")
        if dish_master:
            device_proxy = DeviceProxy(dish_master)
            device_proxy.SetDirectState(DevState.STANDBY)

        LOGGER.info(
            f"After invoking TelescopeStandBy command {central_node} State is:\
            {central_node.State()}"
        )

    @sync_release_resources
    def invoke_releaseResources(
        self,
        release_input_str,
        **kwargs,
    ):
        central_node = DeviceProxy(self.centralnode)
        result, message = central_node.ReleaseResources(release_input_str)
        LOGGER.info(f"ReleaseResources command is invoked on {central_node}")
        return result, message

    @sync_assign_resources()
    def compose_sub(self, assign_res_input, **kwargs):
        resource(self.subarray_node).assert_attribute("State").equals("ON")
        resource(self.subarray_node).assert_attribute("obsState").equals(
            "EMPTY"
        )
        central_node = DeviceProxy(self.centralnode)
        result, message = central_node.AssignResources(assign_res_input)
        LOGGER.info("Invoked AssignResources on CentralNode")
        return result, message

    @sync_configure()
    def configure_subarray(self, configure_input_str, **kwargs):
        subarray_node = DeviceProxy(self.subarray_node)
        result, message = subarray_node.Configure(configure_input_str)
        LOGGER.info("Invoked Configure on SubarrayNode")
        return result, message

    @sync_scan()
    def scan(self, scan_input_str, **kwargs):
        subarray_node = DeviceProxy(self.subarray_node)
        result, message = subarray_node.Scan(scan_input_str)
        LOGGER.info("Invoked Scan on SubarrayNode")
        return result, message

    @sync_end()
    def end(self, **kwargs):
        subarray_node = DeviceProxy(self.subarray_node)
        result, message = subarray_node.End()
        LOGGER.info(f"End command is invoked on {subarray_node}")
        return result, message

    @sync_abort()
    def invoke_abort(self, **kwargs):
        subarray_node = DeviceProxy(self.subarray_node)
        result, message = subarray_node.Abort()
        LOGGER.info("Invoked Abort on SubarrayNode")
        return result, message

    @sync_restart()
    def invoke_restart(self, **kwargs):
        subarray_node = DeviceProxy(self.subarray_node)
        subarray_node.Restart()
        LOGGER.info("Invoked Restart on SubarrayNode")

    @sync_assigning()
    def assign_resources(self, assign_res_input, **kwargs):
        resource(self.subarray_node).assert_attribute("State").equals("ON")
        central_node = DeviceProxy(self.centralnode)
        result, message = central_node.AssignResources(assign_res_input)
        LOGGER.info("Invoked AssignResources on CentralNode")
        return result, message

    @sync_configure_sub()
    def configure_sub(self, configure_input_str, **kwargs):
        resource(self.subarray_node).assert_attribute("obsState").equals(
            "IDLE"
        )
        subarray_node = DeviceProxy(self.subarray_node)
        result, message = subarray_node.Configure(configure_input_str)
        LOGGER.info("Invoked Configure on SubarrayNode")
        return result, message

    @sync_endscan()
    def invoke_endscan(self, **kwargs):
        subarray_node = DeviceProxy(self.subarray_node)
        result, message = subarray_node.EndScan()
        LOGGER.info("Invoked EndScan on SubarrayNode")
        return result, message

    @sync_endscan_in_ready()
    def invoke_endscan_in_ready(self, **kwargs):
        subarray_node = DeviceProxy(self.subarray_node)
        result, message = subarray_node.EndScan()
        LOGGER.info("Invoked EndScan on SubarrayNode")
        return result, message


def tear_down(
    input_json: Optional[str] = None,
    raise_exception: Optional[bool] = True,
    **kwargs,
):
    """Tears down the system after test run to get telescope back in \
        standby state."""

    LOGGER.info("Calling tear down")
    subarray_node_obsstate = resource(kwargs.get("tmc_subarraynode")).get(
        "obsState"
    )
    tmc_helper = TmcHelper(
        kwargs.get("central_node"), kwargs.get("tmc_subarraynode")
    )
    telescope_control = BaseTelescopeControl()

    if subarray_node_obsstate in ["RESOURCING", "CONFIGURING", "SCANNING"]:
        LOGGER.info("Invoking Abort on TMC")

        tmc_helper.invoke_abort(**ON_OFF_DEVICE_COMMAND_DICT)
        LOGGER.info("Invoking Abort command on TMC SubarrayNode")
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_ABORT_INFO, "obsState"
        )

        tmc_helper.invoke_restart(**ON_OFF_DEVICE_COMMAND_DICT)
        LOGGER.info("Invoking Restart command on TMC SubarrayNode")
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
        )

        tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)
        LOGGER.info("Invoking Standby command on TMC SubarrayNode")
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )

        LOGGER.info("Tear Down complete. Telescope is in Standby State")

    elif subarray_node_obsstate == "EMPTY":
        LOGGER.info("Invoking Standby command on TMC SubarrayNode")
        tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )

        LOGGER.info("Tear Down complete. Telescope is in Standby State")

    elif subarray_node_obsstate == "IDLE":
        LOGGER.info("Invoking ReleaseResources command on TMC SubarrayNode")
        tmc_helper.invoke_releaseResources(
            input_json, **ON_OFF_DEVICE_COMMAND_DICT
        )
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
        )

        LOGGER.info("Invoking Standby command on TMC SubarrayNode")
        tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )

        LOGGER.info("Tear Down complete. Telescope is in Standby State")

    elif subarray_node_obsstate == "READY":
        LOGGER.info("Invoking End command on TMC SubarrayNode")
        tmc_helper.end(**ON_OFF_DEVICE_COMMAND_DICT)
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_IDLE_INFO, "obsState"
        )

        LOGGER.info("Invoking ReleaseResources command on TMC SubarrayNode")
        tmc_helper.invoke_releaseResources(
            input_json, **ON_OFF_DEVICE_COMMAND_DICT
        )
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
        )

        LOGGER.info("Invoking Standby command on TMC SubarrayNode")
        tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )

        LOGGER.info("Tear Down complete. Telescope is in Standby State")

    elif subarray_node_obsstate == "EMPTY":
        LOGGER.info("Invoking Standby command on TMC SubarrayNode")
        tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )

        LOGGER.info("Tear Down complete. Telescope is in Standby State")
    elif subarray_node_obsstate in ["ABORTED", "FAULT"]:
        tmc_helper.invoke_restart(**ON_OFF_DEVICE_COMMAND_DICT)
        LOGGER.info("Invoking Restart command on TMC SubarrayNode")
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
        )

        tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)
        LOGGER.info("Invoking Standby command on TMC SubarrayNode")
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )

        LOGGER.info("Tear Down complete. Telescope is in Standby State")

    LOGGER.info("Tear Down Successful, raising an exception for failure")
    if raise_exception:
        raise Exception(
            f"Test case failed and Subarray obsState was: "
            f"{subarray_node_obsstate}"
        )
