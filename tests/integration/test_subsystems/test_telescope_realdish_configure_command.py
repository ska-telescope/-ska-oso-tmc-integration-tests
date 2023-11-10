"""Test Telescope On Command on DISH LMC"""
import time

import pytest
from tango import DeviceProxy

from tests.conftest import wait_for_dish_mode_change
from tests.resources.test_support.common_utils.common_helpers import Waiter
from tests.resources.test_support.constant import (
    centralnode,
    dish_fqdn,
    tmc_subarraynode1,
)
from tests.resources.test_support.enum import DishMode


@pytest.mark.aki
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
    dishfqdn = DeviceProxy(dish_fqdn)

    # Waiting for DISH LMC to respond
    wait_for_dish_mode_change(DishMode.STANDBY_FP, dishfqdn, 30)

    # Check the dishMode of DISH LMC i.e STANDBYFP
    assert dishfqdn.dishMode.value == DishMode.STANDBY_FP

    # invoke assignresources command from central node
    central_node_device.AssignResources(assign_json)

    the_waiter.set_wait_for_specific_obsstate("IDLE", [subarray])
    the_waiter.wait(400)
    # invoke configure command from subarray node
    subarray.Configure(config_json)

    wait_for_dish_mode_change(DishMode.OPERATE, dishfqdn, 30)

    the_waiter.set_wait_for_pointingstate("TRACK", [dishfqdn])
    the_waiter.wait(400)


    # invoke end command from subarray node
    subarray.End()
    the_waiter.set_wait_for_pointingstate("READY", [dishfqdn])
    the_waiter.wait(400)

    # Invoke TelescopeOff command
    central_node_device.ReleaseResources(release_json)
    time.sleep(5)
    central_node_device.TelescopeOff()

    # Waiting for DISH LMC to respond
    wait_for_dish_mode_change(DishMode.STANDBY_LP, dishfqdn, 30)

    # check the dishMode of DISH LMC i.e STANDBYLP
    assert dishfqdn.dishMode.value == DishMode.STANDBY_LP
