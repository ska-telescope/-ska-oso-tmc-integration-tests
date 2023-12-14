"""Test Telescope On Command on DISH LMC"""

import logging

import pytest
from tango import DeviceProxy

from tests.conftest import wait_for_dish_mode_change
from tests.resources.test_support.common_utils.common_helpers import Waiter
from tests.resources.test_support.constant import (  # dish_fqdn_100,
    centralnode,
    dish_fqdn_1,
    dish_fqdn_36,
    dish_fqdn_63,
)
from tests.resources.test_support.enum import DishMode

LOGGER = logging.getLogger(__name__)


@pytest.mark.real_dish
def test_telescope_on():
    """TelescopeOn() and TelescopeOff() is executed on dishlmc  device."""
    the_waiter = Waiter()
    central_node_device = DeviceProxy(centralnode)

    # Invoke TelescopeOn command
    central_node_device.TelescopeOn()

    # Check the dishMode and dishleafnode state
    dish_master_1 = DeviceProxy(dish_fqdn_1)
    LOGGER.info("Dish 1: %s", dish_master_1.dev_name())
    dish_master_36 = DeviceProxy(dish_fqdn_36)
    LOGGER.info("Dish 36: %s", dish_master_36.dev_name())
    dish_master_63 = DeviceProxy(dish_fqdn_63)
    LOGGER.info("Dish 63: %s", dish_master_63.dev_name())
    # dish_master_100 = DeviceProxy(dish_fqdn_100)

    # Waiting for DISH LMC to respond
    wait_for_dish_mode_change(DishMode.STANDBY_FP, dish_master_1, 30)
    wait_for_dish_mode_change(DishMode.STANDBY_FP, dish_master_36, 30)
    wait_for_dish_mode_change(DishMode.STANDBY_FP, dish_master_63, 30)
    # wait_for_dish_mode_change(DishMode.STANDBY_FP, dish_master_100, 30)

    the_waiter.wait(50)

    # Check the dishMode of DISH LMC i.e STANDBYFP
    assert dish_master_1.dishMode.value == DishMode.STANDBY_FP
    assert dish_master_36.dishMode.value == DishMode.STANDBY_FP
    assert dish_master_63.dishMode.value == DishMode.STANDBY_FP
    # assert dish_master_100.dishMode.value == DishMode.STANDBY_FP

    # Invoke TelescopeOff command

    central_node_device.TelescopeOff()

    # Waiting for DISH LMC to respond
    wait_for_dish_mode_change(DishMode.STANDBY_LP, dish_master_1, 30)
    wait_for_dish_mode_change(DishMode.STANDBY_LP, dish_master_36, 30)
    wait_for_dish_mode_change(DishMode.STANDBY_LP, dish_master_63, 30)
    # wait_for_dish_mode_change(DishMode.STANDBY_LP, dish_master_100, 30)

    # check the dishMode of DISH LMC i.e STANDBYLP
    assert dish_master_1.dishMode.value == DishMode.STANDBY_LP
    assert dish_master_36.dishMode.value == DishMode.STANDBY_LP
    assert dish_master_63.dishMode.value == DishMode.STANDBY_LP
    # assert dish_master_100.dishMode.value == DishMode.STANDBY_LP
