import logging

from ska_control_model import ObsState
from ska_ser_logging import configure_logging
from ska_tango_base.control_model import HealthState
from tango import DeviceProxy, DevState

from tests.resources.test_harness.central_node_mid import CentralNodeWrapperMid
from tests.resources.test_support.constant import dish_fqdn_1, dish_fqdn_2

configure_logging(logging.DEBUG)
LOGGER = logging.getLogger(__name__)


class CentralNodeWrapperDish(CentralNodeWrapperMid):
    """A wrapper class to implement common tango specific details
    and standard set of commands for TMC Mid CentralNode with real Dish device,
    defined by the SKA Control Model."""

    def __init__(self) -> None:
        super().__init__()
        self.dish_master_1 = DeviceProxy(dish_fqdn_1)
        self.dish_master_2 = DeviceProxy(dish_fqdn_2)

    def move_to_on(self):
        """
        A method to invoke TelescopeOn command to
        put telescope in ON state
        """
        self.central_node.TelescopeOn()
        device_to_on_list = [
            self.subarray_devices.get("csp_subarray"),
            self.subarray_devices.get("sdp_subarray"),
        ]
        for device in device_to_on_list:
            device_proxy = DeviceProxy(device)
            device_proxy.SetDirectState(DevState.ON)

    def _reset_health_state_for_mock_devices(self):
        """Reset Mock devices"""
        for mock_device in [
            self.sdp_master,
            self.csp_master,
        ]:
            device = DeviceProxy(mock_device)
            device.SetDirectHealthState(HealthState.UNKNOWN)

    def tear_down(self):
        """Handle Tear down of central Node"""
        LOGGER.info("Calling Tear down for central node.")
        self._reset_health_state_for_mock_devices()
        if self.subarray_node.obsState == ObsState.IDLE:
            LOGGER.info("Calling ReleaseResources on CentralNode")
            self.invoke_release_resources(self.release_input)
        elif self.subarray_node.obsState == ObsState.RESOURCING:
            LOGGER.info("Calling Abort and Restart on SubarrayNode")
            self.subarray_abort()
            self.subarray_restart()
        elif self.subarray_node.obsState == ObsState.ABORTED:
            self.subarray_restart()
        self.move_to_off()

    def move_to_off(self):
        """
        A method to invoke TelescopeOff command to
        put telescope in OFF state

        """
        self.central_node.TelescopeOff()
        device_to_on_list = [
            self.subarray_devices.get("csp_subarray"),
            self.subarray_devices.get("sdp_subarray"),
        ]
        for device in device_to_on_list:
            device_proxy = DeviceProxy(device)
            device_proxy.SetDirectState(DevState.OFF)
