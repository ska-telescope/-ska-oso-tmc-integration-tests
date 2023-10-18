"""Test Telescope On Command in mid"""
import os

import pytest
from tango import DeviceProxy

from tests.conftest import wait_for_dish_mode_change
from tests.resources.test_support.constant import centralnode
from tests.resources.test_support.enum import DishMode

dish_name = os.getenv("DISH_NAMESPACE")

dish_fqdn = (
    f"tango://databaseds-tango-base.{dish_name}.svc.cluster"
    ".local:10000/ska001/elt/master"
)


@pytest.mark.real_dish
def test_telescope_on():
    """TelescopeOn() and TelescopeOff() is executed on real dish device."""

    central_node_device = DeviceProxy(centralnode)

    # Invoke TelescopeOn command
    central_node_device.TelescopeOn()

    # Check the dishMode and dishleafnode state
    dishfqdn = DeviceProxy(dish_fqdn)

    # Waiting for DISH LMC to respond
    wait_for_dish_mode_change(DishMode.STANDBY_FP, dishfqdn, 30)

    # Check the dishMode of DISH LMC i.e STANDBYFP
    assert dishfqdn.dishMode.value == DishMode.STANDBY_FP

    # Invoke TelescopeOff command

    central_node_device.TelescopeOff()

    # Waiting for DISH LMC to respond
    wait_for_dish_mode_change(DishMode.STANDBY_LP, dishfqdn, 30)

    # check the dishMode of DISH LMC i.e STANDBYLP
    assert dishfqdn.dishMode.value == DishMode.STANDBY_LP
