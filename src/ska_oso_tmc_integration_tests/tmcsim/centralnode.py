"""
Simulates the behaviour of a TMC CentralNode for the purpose of integration tests.
"""

import ska_tango_testing
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
        # pylint: disable=line-too-long
        # devices inside the TestHarness can't create DeviceProxy instances directly
        # See https://developer.skatelescope.org/projects/ska-tango-testing/en/latest/guide/harness/tango_contexts.html
        # and related Tango bug https://gitlab.com/tango-controls/pytango/-/issues/459
        san = ska_tango_testing.context.DeviceProxy(
            f"{self.base_uri}/tm_subarray_node/1"
        )
        san.AssignResources(cdm_str)

    @command(dtype_in=str)
    def ReleaseResources(self, cdm_str):  # pylint: disable=invalid-name
        """
        Release resources from a subarray.
        """
        san = ska_tango_testing.context.DeviceProxy(
            f"{self.base_uri}/tm_subarray_node/1"
        )
        san.ReleaseResources(cdm_str)
