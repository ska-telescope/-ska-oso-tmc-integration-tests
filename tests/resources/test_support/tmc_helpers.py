import logging
from os.path import dirname, join
from typing import Optional

from tango import DeviceProxy, DevState

import tests.resources.test_support.tmc_helpers as tmc
from tests.resources.test_support.constant import (
    centralnode,
    csp_subarray1,
    dish_master1,
    sdp_subarray1,
    tmc_csp_master_leaf_node,
    tmc_csp_subarray_leaf_node,
    tmc_sdp_master_leaf_node,
    tmc_sdp_subarray_leaf_node,
    tmc_subarraynode1,
)
from tests.resources.test_support.controls import (
    subarray_obs_state_is_aborted,
    subarray_obs_state_is_empty,
    subarray_obs_state_is_idle,
    telescope_is_in_standby_state,
)
from tests.resources.test_support.helpers import resource, waiter, watch
from tests.resources.test_support.sync_decorators import (
    sync_abort,
    sync_assign_resources,
    sync_configure,
    sync_end,
    sync_release_resources,
    sync_restart,
    sync_scan,
    sync_set_to_off,
    sync_set_to_standby,
    sync_telescope_on,
)

LOGGER = logging.getLogger(__name__)


def get_input_str(input_file):
    path = join(dirname(__file__), "..", "..", "data", input_file)
    with open(path, "r", encoding="UTF-8") as f:
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
    tmc_subarraynode_1 = DeviceProxy(tmc_subarraynode1)
    assert 0 < tmc_subarraynode_1.ping()
    csp_master_leaf_node = DeviceProxy(tmc_csp_master_leaf_node)
    assert 0 < csp_master_leaf_node.ping()
    csp_subarray = DeviceProxy(tmc_csp_subarray_leaf_node)
    assert 0 < csp_subarray.ping()
    sdp_master_leaf_node = DeviceProxy(tmc_sdp_master_leaf_node)
    assert 0 < sdp_master_leaf_node.ping()
    sdp_subarray = DeviceProxy(tmc_sdp_subarray_leaf_node)
    assert 0 < sdp_subarray.ping()


@sync_telescope_on
def set_to_on():
    central_node = DeviceProxy(centralnode)
    LOGGER.info(
        "Before Sending TelescopeOn command %s State is: %s",
        central_node,
        central_node.State(),
    )
    central_node.TelescopeOn()
    the_waiter = waiter()
    the_waiter.waits.append(
        watch(resource(dish_master1)).to_become("State", changed_to="STANDBY")
    )
    the_waiter.wait(200)
    csp_subarray_1 = DeviceProxy(csp_subarray1)
    csp_subarray_1.SetDirectState(DevState.ON)
    sdp_subarray_1 = DeviceProxy(sdp_subarray1)
    sdp_subarray_1.SetDirectState(DevState.ON)
    dish_master_1 = DeviceProxy(dish_master1)
    dish_master_1.SetDirectState(DevState.ON)
    dish_master_1.SetDirectPointingState(int(1))


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
        "After invoking TelescopeOff command %s State is: %s",
        central_node,
        central_node.State(),
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
        "After invoking TelescopeStandBy command  %s State is: %s",
        central_node,
        central_node.State(),
    )


@sync_release_resources
def invoke_releaseResources(release_input_str):
    central_node = DeviceProxy(centralnode)
    central_node.ReleaseResources(release_input_str)
    LOGGER.info(f"ReleaseResources command is invoked on {central_node}")
    csp_subarray_1 = DeviceProxy(csp_subarray1)
    csp_subarray_1.SetDirectState(DevState.OFF)
    sdp_subarray_1 = DeviceProxy(sdp_subarray1)
    sdp_subarray_1.SetDirectState(DevState.OFF)
    dish_master_1 = DeviceProxy(dish_master1)
    dish_master_1.SetDirectState(DevState.STANDBY)


@sync_end()
def end():
    subarray_node = DeviceProxy(tmc_subarraynode1)
    subarray_node.End()
    LOGGER.info(f"End command is invoked on {subarray_node}")


@sync_assign_resources()
def compose_sub(assign_res_input):
    resource(tmc_subarraynode1).assert_attribute("State").equals("ON")
    resource(tmc_subarraynode1).assert_attribute("obsState").equals("EMPTY")
    central_node = DeviceProxy(centralnode)
    central_node.AssignResources(assign_res_input)
    LOGGER.info("Invoked AssignResources on CentralNode")


@sync_configure()
def configure_subarray(configure_input_str):
    resource(tmc_subarraynode1).assert_attribute("obsState").equals("IDLE")
    subarray_node = DeviceProxy(tmc_subarraynode1)
    subarray_node.Configure(configure_input_str)
    LOGGER.info("Invoked Configure on SubarrayNode")


@sync_scan()
def scan(scan_input):
    resource(tmc_subarraynode1).assert_attribute("obsState").equals("READY")
    subarray_node = DeviceProxy(tmc_subarraynode1)
    subarray_node.Scan(scan_input)
    LOGGER.info("Invoked Scan on SubarrayNode")


@sync_abort()
def invoke_abort():
    subarray_node = DeviceProxy(tmc_subarraynode1)
    DeviceProxy(dish_master1).TrackStop()
    subarray_node.Abort()
    LOGGER.info("Invoked Abort on SubarrayNode")


@sync_restart()
def invoke_restart():
    subarray_node = DeviceProxy(tmc_subarraynode1)
    subarray_node.Restart()
    DeviceProxy(dish_master1).SetDirectPointingState(int(1))
    LOGGER.info("Invoked Restart on SubarrayNode")


def tear_down(input_json: Optional[str] = None):
    """Tears down the system after test run to get telescope back in standby
    state."""
    subarray_node_obsstate = resource(tmc_subarraynode1).get("obsState")

    if subarray_node_obsstate in ["RESOURCING", "CONFIGURING", "SCANNING"]:
        LOGGER.info("Invoking Abort on TMC")
        tmc.invoke_abort()

        assert subarray_obs_state_is_aborted()

        LOGGER.info("Invoking Restart on TMC")
        tmc.invoke_restart()

        assert subarray_obs_state_is_empty()

        LOGGER.info("Invoking Telescope Standby on TMC")
        tmc.set_to_standby()

        assert telescope_is_in_standby_state()
        LOGGER.info("Tear Down complete. Telescope is in Standby State")

    elif subarray_node_obsstate == "EMPTY":
        LOGGER.info("Invoking Telescope Standby on TMC")
        tmc.set_to_standby()

        assert telescope_is_in_standby_state()
        LOGGER.info("Tear Down complete. Telescope is in Standby State")

    elif subarray_node_obsstate == "IDLE":
        LOGGER.info("Invoking ReleaseResources on TMC")
        tmc.invoke_releaseResources(input_json)

        LOGGER.info("Invoking Telescope Standby on TMC")
        tmc.set_to_standby()

        assert telescope_is_in_standby_state()
        LOGGER.info("Tear Down complete. Telescope is in Standby State")

    elif subarray_node_obsstate == "READY":
        LOGGER.info("Invoking END on TMC")
        tmc.end()

        assert subarray_obs_state_is_idle()

        LOGGER.info("Invoking ReleaseResources on TMC")
        tmc.invoke_releaseResources(input_json)

        LOGGER.info("Invoking Telescope Standby on TMC")
        tmc.set_to_standby()

        assert telescope_is_in_standby_state()
        LOGGER.info("Tear Down complete. Telescope is in Standby State")

    elif subarray_node_obsstate == "EMPTY":
        LOGGER.info("Invoking Telescope Standby on TMC")
        tmc.set_to_standby()

        assert telescope_is_in_standby_state()
        LOGGER.info("Tear Down complete. Telescope is in Standby State")

    elif subarray_node_obsstate in ["ABORTED", "FAULT"]:
        LOGGER.info("Invoking Restart on TMC")
        tmc.invoke_restart()

        assert subarray_obs_state_is_empty()

        LOGGER.info("Invoking Telescope Standby on TMC")
        tmc.set_to_standby()

        assert telescope_is_in_standby_state()
        LOGGER.info("Tear Down complete. Telescope is in Standby State")

    LOGGER.info("Tear Down Successful, raising an exception for failure")
    raise Exception(
        f"Test case failed and Subarray obsState was: {subarray_node_obsstate}"
    )
