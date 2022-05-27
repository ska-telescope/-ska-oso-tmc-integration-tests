from os.path import dirname, join
from tests.resources.test_support.sync_decorators import (
    sync_telescope_on,
    sync_set_to_off,
    sync_set_to_standby,
    sync_release_resources,
)
from tango import DeviceProxy, DevState
from tests.resources.test_support.controls import centralnode, csp_subarray1, sdp_subarray1

import logging

LOGGER = logging.getLogger(__name__)


def get_input_str(input_file):
    path = join(dirname(__file__), "..", "..", "data", input_file)
    with open(path, "r") as f:
        return f.read()

@sync_telescope_on
def set_to_on():
    CentralNode = DeviceProxy(centralnode)
    LOGGER.info(
        f"Before Sending TelescopeOn command {centralnode} State is: {CentralNode.State()}"
    )
    CentralNode.TelescopeOn()
    csp_Subarray1_proxy = DeviceProxy(csp_subarray1)
    csp_Subarray1_proxy.SetDirectState(DevState.ON)
    sdp_Subarray1_proxy = DeviceProxy(sdp_subarray1)
    sdp_Subarray1_proxy.SetDirectState(DevState.ON)

@sync_set_to_off
def set_to_off():
    CentralNode = DeviceProxy(centralnode)
    CentralNode.TelescopeOff()
    csp_Subarray1_proxy = DeviceProxy(sdp_subarray1)
    csp_Subarray1_proxy.SetDirectState(DevState.OFF)
    LOGGER.info(
            f"After invoking TelescopeOff command {centralnode} State is: {CentralNode.State()}"
    )
    
@sync_set_to_standby
def set_to_standby():
    CentralNode = DeviceProxy(centralnode)
    CentralNode.TelescopeStandBy()
    csp_Subarray1_proxy = DeviceProxy(csp_subarray1)
    csp_Subarray1_proxy.SetDirectState(DevState.OFF)
    LOGGER.info(
            f"After invoking TelescopeStandBy command {centralnode} State is: {CentralNode.State()}"
    )

@sync_release_resources
def invoke_releaseResources(release_input_str):
    CentralNode = DeviceProxy(centralnode)
    CentralNode.ReleaseResources(release_input_str)
    LOGGER.info(
            f"ReleaseResources command is invoked on {centralnode}"
    )