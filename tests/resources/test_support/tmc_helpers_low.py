from os.path import dirname, join
from tests.resources.test_support.sync_decorators_low import (
    sync_telescope_on,
    sync_set_to_off,
    sync_set_to_standby,
    sync_release_resources,
    sync_end, sync_assign_resources, sync_configure, sync_scan
)
from tango import DeviceProxy, DevState
from tests.resources.test_support.controls_low import centralnode, csp_subarray1, sdp_subarray1, tmc_subarraynode1
from tests.resources.test_support.helpers_low import resource
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
    tmc_subarraynode_1 = DeviceProxy(tmc_subarraynode1)
    assert 0 < tmc_subarraynode_1.ping()
    csp_master = DeviceProxy("ska_low/tm_leaf_node/csp_master")
    assert 0 < csp_master.ping()
    csp_subarray = DeviceProxy("ska_low/tm_leaf_node/csp_subarray01")
    assert 0 < csp_subarray.ping()
    sdp_master = DeviceProxy("ska_low/tm_leaf_node/sdp_master")
    assert 0 < sdp_master.ping()
    sdp_subarray = DeviceProxy("ska_low/tm_leaf_node/sdp_subarray01")
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

@sync_set_to_off
def set_to_off():
    central_node = DeviceProxy(centralnode)
    central_node.TelescopeOff()
    csp_subarray_1 = DeviceProxy(csp_subarray1)
    csp_subarray_1.SetDirectState(DevState.OFF)
    sdp_subarray_1 = DeviceProxy(sdp_subarray1)
    sdp_subarray_1.SetDirectState(DevState.OFF)
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
def end():
    subarray_node = DeviceProxy(tmc_subarraynode1)
    subarray_node.End()
    LOGGER.info(
            f"End command is invoked on {subarray_node}"
    )

@sync_assign_resources()
def compose_sub(assign_res_input):
    resource(tmc_subarraynode1).assert_attribute("State").equals(
        "ON"
    )
    resource(tmc_subarraynode1).assert_attribute("obsState").equals(
        "EMPTY"
    )
    central_node = DeviceProxy("ska_low/tm_central/central_node")
    central_node.AssignResources(assign_res_input)
    LOGGER.info("Invoked AssignResources on CentralNode")


@sync_configure()
def configure_subarray(configure_input_str):
    resource(tmc_subarraynode1).assert_attribute("obsState").equals(
        "IDLE"
    )
    subarray_node = DeviceProxy(tmc_subarraynode1)
    subarray_node.Configure(configure_input_str)
    LOGGER.info("Invoked Configure on SubarrayNode")


@sync_scan()
def scan(scan_input):
    resource(tmc_subarraynode1).assert_attribute("obsState").equals(
        "READY"
    )
    subarray_node = DeviceProxy(tmc_subarraynode1)
    subarray_node.Scan(scan_input)
    LOGGER.info("Invoked Scan on SubarrayNode")