from ska_tango_base.control_model import HealthState
from tango import DeviceProxy, DevState

from tests.resources.test_harness.central_node import CentralNode
from tests.resources.test_harness.constant import (
    csp_master,
    csp_subarray1,
    dish_master1,
    dish_master2,
    sdp_master,
    sdp_subarray1,
    tmc_csp_master_leaf_node,
    tmc_sdp_master_leaf_node,
)


class CentralNodeMid(CentralNode):
    """A TMC CentralNode class to implements the standard set
    of commands defined by the SKA Control Model for Mid Telescope"""

    def __init__(self, central_node) -> None:
        super().__init__(central_node)
        self.csp_master_leaf_node = DeviceProxy(tmc_csp_master_leaf_node)
        self.sdp_master_leaf_node = DeviceProxy(tmc_sdp_master_leaf_node)
        self.subarray_devices = {
            "csp_subarray": DeviceProxy(csp_subarray1),
            "sdp_subarray": DeviceProxy(sdp_subarray1),
        }
        self.sdp_master = DeviceProxy(sdp_master)
        self.csp_master = DeviceProxy(csp_master)
        self.dish_master1 = DeviceProxy(dish_master1)
        self.dish_master2 = DeviceProxy(dish_master2)
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
