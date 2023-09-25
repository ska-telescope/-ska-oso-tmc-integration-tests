from tango import DeviceProxy, DevState

from tests.resources.test_harness.central_node import CentralNodeWrapper
from tests.resources.test_harness.constant import (
    device_dict_low,
    low_centralnode,
    low_csp_master,
    low_csp_master_leaf_node,
    low_csp_subarray1,
    low_sdp_master,
    low_sdp_master_leaf_node,
    low_sdp_subarray1,
)
from tests.resources.test_harness.utils.sync_decorators import (
    sync_assign_resources,
)


# TODO: Currently the code for MCCS has been commented as it will be enabled
#  in the upcoming sprints of PI-20
class CentralNodeWrapperLow(CentralNodeWrapper):
    """A TMC CentralNode class to implements the standard set
    of commands defined by the SKA Control Model for Low Telescope"""

    def __init__(self) -> None:
        super().__init__()
        self.central_node = DeviceProxy(low_centralnode)
        self.csp_master_leaf_node = DeviceProxy(low_csp_master_leaf_node)
        self.sdp_master_leaf_node = DeviceProxy(low_sdp_master_leaf_node)
        # self.mccs_master_leaf_node = DeviceProxy(mccs_master_leaf_node)
        self.subarray_devices = {
            "csp_subarray": DeviceProxy(low_csp_subarray1),
            "sdp_subarray": DeviceProxy(low_sdp_subarray1),
            # "mccs_subarray": DeviceProxy(mccs_subarray1)
        }
        self.sdp_master = DeviceProxy(low_sdp_master)
        self.csp_master = DeviceProxy(low_csp_master)
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
