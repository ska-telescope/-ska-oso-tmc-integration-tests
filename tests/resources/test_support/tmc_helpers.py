from os.path import dirname, join
from tests.resources.test_support.sync_decorators import (
    sync_telescope_on,
    sync_set_to_off,
    sync_set_to_standby,
    sync_release_resources,
    sync_end
)
from tango import DeviceProxy, DevState
from tests.resources.test_support.controls import centralnode, csp_subarray1, sdp_subarray1, dish_master1, tm_subarraynode1

import logging

LOGGER = logging.getLogger(__name__)


def get_input_str(input_file):
    path = join(dirname(__file__), "..", "..", "data", input_file)
    with open(path, "r") as f:
        return f.read()

def check_devices():
    central_node = DeviceProxy(centralnode)
    assert 0 < central_node.ping()
    csp_subarray_1 = DeviceProxy(csp_subarray1)
    assert 0 < csp_subarray_1.ping()

    sdp_subarray_1 = DeviceProxy(sdp_subarray1)
    assert 0 < sdp_subarray_1.ping()

    dish_master_1 = DeviceProxy(dish_master1)
    assert 0 < dish_master_1.ping()

    tm_subarraynode_1 = DeviceProxy(tm_subarraynode1)
    assert 0 < tm_subarraynode_1.ping()

    csp_master = DeviceProxy("ska_mid/tm_leaf_node/csp_master")
    assert 0 < csp_master.ping()

    csp_subarray = DeviceProxy("ska_mid/tm_leaf_node/csp_subarray01")
    assert 0 < csp_subarray.ping()

    sdp_master = DeviceProxy("ska_mid/tm_leaf_node/sdp_master")
    assert 0 < sdp_master.ping()

    sdp_subarray = DeviceProxy("ska_mid/tm_leaf_node/sdp_subarray01")
    assert 0 < sdp_subarray.ping()




@sync_telescope_on
def set_to_on():
    central_node = DeviceProxy(centralnode)
    LOGGER.info(
        f"Before Sending TelescopeOn command {central_node} State is: {central_node.State()}"
    )
    central_node.TelescopeOn()
    csp_subarray_1 = DeviceProxy(csp_subarray1)
    csp_subarray_1.SetDirectState(DevState.ON)
    sdp_subarray_1 = DeviceProxy(sdp_subarray1)
    sdp_subarray_1.SetDirectState(DevState.ON)
    dish_master_1 = DeviceProxy(dish_master1)
    dish_master_1.SetDirectState(DevState.ON)

@sync_set_to_off
def set_to_off():
    central_node = DeviceProxy(centralnode)
    central_node.TelescopeOff()
    csp_subarray_1 = DeviceProxy(csp_subarray1)
    csp_subarray_1.SetDirectState(DevState.OFF)
    sdp_subarray_1 = DeviceProxy(sdp_subarray1)
    sdp_subarray_1.SetDirectState(DevState.OFF)
    dish_master_1 = DeviceProxy(dish_master1)
    dish_master_1.SetDirectState(DevState.STANDBY)
    LOGGER.info(
            f"After invoking TelescopeOff command {central_node} State is: {central_node.State()}"
    )

@sync_set_to_standby
def set_to_standby():
    central_node = DeviceProxy(centralnode)
    central_node.TelescopeStandBy()
    csp_subarray_1 = DeviceProxy(csp_subarray1)
    csp_subarray_1.SetDirectState(DevState.OFF)
    sdp_subarray_1 = DeviceProxy(sdp_subarray1)
    sdp_subarray_1.SetDirectState(DevState.OFF)
    dish_master_1 = DeviceProxy(dish_master1)
    dish_master_1.SetDirectState(DevState.STANDBY)
    LOGGER.info(
            f"After invoking TelescopeStandBy command {central_node} State is: {central_node.State()}"
    )

@sync_release_resources
def invoke_releaseResources(release_input_str):
    central_node = DeviceProxy(centralnode)
    central_node.ReleaseResources(release_input_str)
    LOGGER.info(
            f"ReleaseResources command is invoked on {central_node}"
    )

@sync_end()
def invoke_end():
    subarraynode_node = DeviceProxy(tm_subarraynode1)
    subarraynode_node.End()
    LOGGER.info(
            f"ReleaseResources command is invoked on {subarraynode_node}"
    )