"""Test Telescope On Command on DISH LMC"""

import pytest
from tango import DeviceProxy

from tests.conftest import wait_for_dish_mode_change
from tests.resources.test_support.common_utils.common_helpers import Waiter
from tests.resources.test_support.constant import (
    centralnode,
    dish_fqdn_1,
    dish_fqdn_2,
)
from tests.resources.test_support.enum import DishMode


@pytest.mark.real_dish
def test_telescope_on():
    """TelescopeOn() and TelescopeOff() is executed on dishlmc  device."""
    the_waiter = Waiter()
    central_node_device = DeviceProxy(centralnode)

    # Invoke TelescopeOn command
    central_node_device.TelescopeOn()

    # Check the dishMode and dishleafnode state
    dish_master_1 = DeviceProxy(dish_fqdn_1)
    dish_master_2 = DeviceProxy(dish_fqdn_2)

    # Waiting for DISH LMC to respond
    wait_for_dish_mode_change(DishMode.STANDBY_FP, dish_master_1, 30)
    wait_for_dish_mode_change(DishMode.STANDBY_FP, dish_master_2, 30)

    the_waiter.wait(50)

    # Check the dishMode of DISH LMC i.e STANDBYFP
    assert dish_master_1.dishMode.value == DishMode.STANDBY_FP
    assert dish_master_2.dishMode.value == DishMode.STANDBY_FP

    # Invoke TelescopeOff command

    central_node_device.TelescopeOff()

    # Waiting for DISH LMC to respond
    wait_for_dish_mode_change(DishMode.STANDBY_LP, dish_master_1, 30)
    wait_for_dish_mode_change(DishMode.STANDBY_LP, dish_master_2, 30)

    # check the dishMode of DISH LMC i.e STANDBYLP
    assert dish_master_1.dishMode.value == DishMode.STANDBY_LP
    assert dish_master_2.dishMode.value == DishMode.STANDBY_LP
