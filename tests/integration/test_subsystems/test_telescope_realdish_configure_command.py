"""Test Telescope On Command on DISH LMC"""
import time

import pytest
from tango import DeviceProxy

from tests.conftest import wait_for_dish_mode_change
from tests.resources.test_support.common_utils.common_helpers import Waiter
from tests.resources.test_support.constant import (
    centralnode,
    dish_fqdn_1,
    dish_fqdn_2,
    tmc_subarraynode1,
)
from tests.resources.test_support.enum import DishMode


@pytest.mark.real_dish
def test_configure(json_factory):
    """TelescopeOn() and TelescopeOff() is executed on dishlmc  device."""
    assign_json = json_factory("command_AssignResources")
    config_json = json_factory("command_Configure")
    release_json = json_factory("command_ReleaseResources")
    the_waiter = Waiter()
    central_node_device = DeviceProxy(centralnode)
    subarray = DeviceProxy(tmc_subarraynode1)

    # Invoke TelescopeOn command
    central_node_device.TelescopeOn()

    # Check the dishMode and dishleafnode state
    dish_master_1 = DeviceProxy(dish_fqdn_1)
    dish_master_2 = DeviceProxy(dish_fqdn_2)

    # Waiting for DISH LMC to respond
    wait_for_dish_mode_change(DishMode.STANDBY_FP, dish_master_1, 30)
    wait_for_dish_mode_change(DishMode.STANDBY_FP, dish_master_2, 30)

    # Check the dishMode of DISH LMC i.e STANDBYFP
    assert dish_master_1.dishMode.value == DishMode.STANDBY_FP
    assert dish_master_2.dishMode.value == DishMode.STANDBY_FP

    # invoke assignresources command from central node
    central_node_device.AssignResources(assign_json)

    the_waiter.set_wait_for_specific_obsstate("IDLE", [subarray])
    the_waiter.wait(400)

    time.sleep(5)

    # invoke configure command from subarray node
    subarray.Configure(config_json)

    wait_for_dish_mode_change(DishMode.OPERATE, dish_master_1, 30)
    wait_for_dish_mode_change(DishMode.OPERATE, dish_master_2, 30)

    the_waiter.set_wait_for_specific_obsstate("READY", [subarray])
    the_waiter.wait(600)
    # invoke end command from subarray node
    subarray.End()

    the_waiter.set_wait_for_specific_obsstate("IDLE", [subarray])
    the_waiter.wait(400)
    # Invoke TelescopeOff command
    central_node_device.ReleaseResources(release_json)
    the_waiter.wait(100)
    # Tearing down
    central_node_device.TelescopeOff()
