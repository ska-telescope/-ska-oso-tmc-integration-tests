from ska_tango_base.control_model import HealthState
from tango import DeviceProxy, DevState

from tests.resources.test_harness.central_node import CentralNodeWrapper
from tests.resources.test_harness.constant import (
    centralnode,
    csp_master,
    csp_subarray1,
    dish_master1,
    dish_master2,
    sdp_master,
    sdp_subarray1,
    tmc_csp_master_leaf_node,
    tmc_sdp_master_leaf_node,
)


class CentralNodeWrapperMid(CentralNodeWrapper):
    """A wrapper class to implement common tango specific details
    and standard set of commands for TMC Mid CentralNode,
    defined by the SKA Control Model."""

    def __init__(self) -> None:
        super().__init__()
        self.central_node = DeviceProxy(centralnode)
        self.csp_master_leaf_node = DeviceProxy(tmc_csp_master_leaf_node)
        self.sdp_master_leaf_node = DeviceProxy(tmc_sdp_master_leaf_node)
        self.subarray_devices = {
            "csp_subarray": DeviceProxy(csp_subarray1),
            "sdp_subarray": DeviceProxy(sdp_subarray1),
        }
        self.sdp_master = DeviceProxy(sdp_master)
        self.csp_master = DeviceProxy(csp_master)
        self.dish_master_list = [
            DeviceProxy(dish_master1),
            DeviceProxy(dish_master2),
        ]
        self._state = DevState.OFF

    def _reset_health_state_for_mock_devices(self):
        """Reset Mock devices"""
        super()._reset_health_state_for_mock_devices()
        for mock_device in self.dish_master_list:
            mock_device.SetDirectHealthState(HealthState.UNKNOWN)
