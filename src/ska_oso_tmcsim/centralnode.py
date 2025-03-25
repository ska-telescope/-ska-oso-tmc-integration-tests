"""
Simulates the behaviour of a TMC CentralNode for the purpose of integration tests.
"""

import tango
from tango import DevState
from tango.server import Device, command, device_property


class CentralNode(Device):
    """
    Simulates the bare minimum TMC CentralNode device server functionality
    required for OSO/TMC integration tests.
    """

    base_uri = device_property(dtype=str)
    """The domain part of the device FQDN, eg TANGO_HOST/domain/family/member"""

    def init_device(self):
        """
        Simulate CentralNode device initialisation.
        """
        Device.init_device(self)
        self.set_state(DevState.ON)

    @command(dtype_in=str)
    def AssignResources(self, cdm_str):  # pylint: disable=invalid-name
        """
        Assign resources to a subarray.
        """
        san = tango.DeviceProxy(f"{self.base_uri}/tm_subarray_node/1")
        san.AssignResources(cdm_str)

    @command(dtype_in=str)
    def ReleaseResources(self, cdm_str):  # pylint: disable=invalid-name
        """
        Release resources from a subarray.
        """
        san = tango.DeviceProxy(f"{self.base_uri}/tm_subarray_node/1")
        san.ReleaseResources(cdm_str)
