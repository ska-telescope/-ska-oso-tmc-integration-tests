"""
Simulates the behaviour of a TMC CentralNode for the purpose of integration tests.
"""

import tango
from tango import DevState
from tango.server import Device, command, device_property

from ska_oso_tmcsim.subarraynode import get_subarraynode_trl


def get_centralnode_trl(domain: str) -> str:
    """
    Get the TRL for a TMC CentralNode.

    Returns pre-ADR-9 TRLs if the Tango domain is an old-style 'ska_mid' or 'ska_low'
    domain.

    @param domain: Tango domain
    @return: full TRL for the TMC CentralNode
    """
    if domain in ["ska_mid", "ska_low"]:
        return f"{domain}/tm_central/central_node"
    else:
        return f"{domain}/central-node/0"


class CentralNode(Device):
    """
    Simulates the bare minimum TMC CentralNode device server functionality
    required for OSO/TMC integration tests.
    """

    domain = device_property(dtype=str)
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
        subarray_trl = get_subarraynode_trl(self.domain, 1)
        san = tango.DeviceProxy(subarray_trl)
        san.AssignResources(cdm_str)

    @command(dtype_in=str)
    def ReleaseResources(self, cdm_str):  # pylint: disable=invalid-name
        """
        Release resources from a subarray.
        """
        subarray_trl = get_subarraynode_trl(self.domain, 1)
        san = tango.DeviceProxy(subarray_trl)
        san.ReleaseResources(cdm_str)
