"""Test Telescope On Command on DISH LMC"""
import time

import pytest
from tango import DeviceProxy, DevState

from tests.conftest import (
    LOGGER,
    wait_for_dish_mode_change,
    wait_for_telescope_state_change,
)
from tests.resources.test_support.common_utils.common_helpers import Waiter
from tests.resources.test_support.constant import (
    centralnode,
    dish_fqdn_1,
    dish_fqdn_36,
    tmc_subarraynode1,
)
from tests.resources.test_support.enum import DishMode


# @pytest.mark.skip(
#     reason="Subarray stuck in configuring due to uneven pointing states."
# )
@pytest.mark.real_dish
# @pytest.mark.skip(
#     reason="Configure fails due to uneven pointingState events in case of "
#     + "multiple dishes. Will be debugged and fixed seperately."
# )
def test_configure(json_factory):
    """TelescopeOn() and TelescopeOff() is executed on dishlmc  device."""
    assign_json = json_factory("command_AssignResources")
    config_json = json_factory("command_Configure")
    release_json = json_factory("command_ReleaseResources")
    the_waiter = Waiter()
    central_node_device = DeviceProxy(centralnode)
    subarray = DeviceProxy(tmc_subarraynode1)

    result = wait_for_telescope_state_change(
        DevState.OFF, central_node_device, 30
    )
    LOGGER.info("Result is: %s", result)
    # Invoke TelescopeOn command
    central_node_device.TelescopeOn()

    # Check the dishMode and dishleafnode state
    dish_master_1 = DeviceProxy(dish_fqdn_1)
    dish_master_2 = DeviceProxy(dish_fqdn_36)
    # dish_master_3 = DeviceProxy(dish_fqdn_63)
    # dish_master_4 = DeviceProxy(dish_fqdn_4)

    # Waiting for DISH LMC to respond
    result = wait_for_dish_mode_change(DishMode.STANDBY_FP, dish_master_1, 30)
    LOGGER.info("Result is: %s", result)
    result = wait_for_dish_mode_change(DishMode.STANDBY_FP, dish_master_2, 30)
    LOGGER.info("Result is: %s", result)

    result = wait_for_telescope_state_change(
        DevState.ON, central_node_device, 30
    )
    LOGGER.info("Result is: %s", result)

    # Check the dishMode of DISH LMC i.e STANDBYFP
    # assert dish_master_1.dishMode.value == DishMode.STANDBY_FP
    # assert dish_master_2.dishMode.value == DishMode.STANDBY_FP

    # invoke assignresources command from central node
    central_node_device.AssignResources(assign_json)

    time.sleep(5)
    the_waiter.set_wait_for_specific_obsstate("IDLE", [subarray])

    # invoke configure command from subarray node
    subarray.Configure(config_json)

    wait_for_dish_mode_change(DishMode.OPERATE, dish_master_1, 30)
    wait_for_dish_mode_change(DishMode.OPERATE, dish_master_2, 30)
    # wait_for_dish_mode_change(DishMode.OPERATE, dish_master_3, 30)
    # wait_for_dish_mode_change(DishMode.OPERATE, dish_master_4, 30)

    the_waiter.set_wait_for_specific_obsstate("READY", [subarray])
    the_waiter.wait(600)
    # invoke end command from subarray node
    subarray.End()

    the_waiter.set_wait_for_specific_obsstate("IDLE", [subarray])
    the_waiter.wait(400)
    # Invoke TelescopeOff command
    central_node_device.ReleaseResources(release_json)
    time.sleep(5)
    # Tearing down
    central_node_device.TelescopeOff()
