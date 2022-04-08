import logging
import time

import pytest
from tango import DeviceProxy, DevState
import pytest
import os
import logging
from tests.resources.test_support.helpers import waiter, watch, resource
from tests.resources.test_support.controls import telescope_is_in_standby, telescope_is_in_on, telescope_is_in_off
import tests.resources.test_support.tmc_helpers as tmc


LOGGER = logging.getLogger(__name__)

central_node = DeviceProxy("ska_mid/tm_central/central_node")
sdp_master = DeviceProxy("mid_sdp/elt/master")
sdp_Subarray = DeviceProxy("mid_sdp/elt/subarray_1")

@pytest.mark.SKA_mid
def test_telescope_on():
    """TelescopeOn() is executed."""
    try:
        fixture = {}
        fixture["state"] = "Unknown"

        # """Verify Telescope is Off"""
        # assert sdp_master.State() in [DevState.DISABLE, DevState.STANDBY, DevState.OFF]
        # assert SdpSubarray.State() in [DevState.DISABLE, DevState.OFF]
        assert telescope_is_in_standby()
        LOGGER.info("Staring up the Telescope")
        """Invoke TelescopeOn() command on TMC"""
        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
        # central_node.TelescopeOn()
        # time.sleep(0.5)
        tmc.set_to_on()

        LOGGER.info("TelescopeOn command is invoked successfully")

        # """Verify Sdp Master and Sdp Subarray State"""
        # assert central_node.State() == DevState.ON
        # assert central_node.telescopeState == DevState.UNKNOWN
        # assert sdp_master.State() == DevState.ON
        # assert sdp_Subarray.State() == DevState.ON

        assert telescope_is_in_on()

        fixture["state"] = "TelescopeOn"

        # """Invoke TelescopeOff() command on TMC"""
        # LOGGER.info("Invoking TelescopeOff command on TMC CentralNode")
        # central_node.TelescopeOff()
        # time.sleep(0.5)
        # LOGGER.info("TelescopeOff command is invoked successfully")

        tmc.set_to_off()

        # """Verify Sdp Master and Sdp Subarray State"""
        # assert central_node.State() == DevState.ON
        # assert central_node.telescopeState == DevState.UNKNOWN
        # assert sdp_master.State() == DevState.OFF
        # assert sdp_Subarray.State() == DevState.OFF

        assert telescope_is_in_off()

        fixture["state"] = "TelescopeOff"

        LOGGER.info("Tests complete: tearing down...")

    except:
        LOGGER.info("Tearing down failed test, state = {}".format(fixture["state"]))
        if fixture["state"] == "TelescopeOn":
            tmc.set_to_off()
        raise

# def tear_down(fixture):
#     LOGGER.info(
#         "Tearing down failed test, state = {}".format(fixture["state"])
#     )
#     if fixture["state"] == "TelescopeOn":
#         central_node.TelescopeOff()
#     else:
#         pytest.fail("unable to complete test without exceptions")

