"""Test Telescope On Command in mid"""
import os
import time

import pytest
from tango import DeviceProxy

from tests.resources.test_support.constant import centralnode

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

    # check the dishMode and dishleafnode state
    dishfqdn = DeviceProxy(dish_fqdn)

    # Sleep is added for waiting for DISH LMC to respond
    time.sleep(6)

    # check the dishMode of DISH LMC i.e STANDBYFP
    assert dishfqdn.dishMode.value == 3

    # Invoke TelescopeOff command

    central_node_device.TelescopeOff()

    time.sleep(6)
    # check the dishMode of DISH LMC i.e STANDBYLP
    assert dishfqdn.dishMode.value == 2
