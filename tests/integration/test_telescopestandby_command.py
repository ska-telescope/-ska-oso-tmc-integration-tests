import logging
import time

import pytest
from tango import DeviceProxy, DevState

LOGGER = logging.getLogger(__name__)

from tango import DeviceProxy, DevState

LOGGER = logging.getLogger(__name__)

TMCCentralNode = DeviceProxy("ska_mid/tm_central/central_node")
SdpMaster = DeviceProxy("mid_sdp/elt/master")
SdpSubarray = DeviceProxy("mid_sdp/elt/subarray_1")

@pytest.mark.SKA_mid
def test_telescope_standby():
    """TelescopeOn() is executed."""
    try:
        fixture = {}
        fixture["state"] = "Unknown"

        """Verify Telescope is Off"""
        assert SdpMaster.State() in [DevState.DISABLE, DevState.STANDBY, DevState.OFF]
        assert SdpSubarray.State() in [DevState.DISABLE, DevState.OFF]

        """Invoke TelescopeOn() command on TMC"""
        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
        TMCCentralNode.TelescopeOn()
        time.sleep(0.5)
        LOGGER.info("TelescopeOn command is invoked successfully")

        """Verify Sdp Master and Sdp Subarray State"""
        assert TMCCentralNode.State() == DevState.ON
        assert TMCCentralNode.telescopeState == DevState.UNKNOWN
        assert SdpMaster.State() == DevState.ON
        assert SdpSubarray.State() == DevState.ON

        fixture["state"] = "TelescopeOn"

        """Invoke TelescopeStandby() command on TMC"""
        LOGGER.info("Invoking TelescopeStandby command on TMC CentralNode")
        TMCCentralNode.TelescopeStandby()
        time.sleep(0.5)
        LOGGER.info("TelescopeStandby command is invoked successfully")

        """Verify Sdp Master and Sdp Subarray State"""
        assert TMCCentralNode.State() == DevState.ON
        assert TMCCentralNode.telescopeState == DevState.UNKNOWN
        assert SdpMaster.State() == DevState.STANDBY
        assert SdpSubarray.State() == DevState.STANDBY

        fixture["state"] = "TelescopeStandby"

        LOGGER.info("Tests complete: tearing down...")

    except Exception:
        LOGGER.info("Tear down the test...")
        tear_down(fixture)
        pytest.fail("unable to complete test without exceptions")


def tear_down(fixture):
    LOGGER.info(
        "Tearing down failed test, state = {}".format(fixture["state"])
    )
    if fixture["state"] == "TelescopeOn":
        TMCCentralNode.TelescopeOff()
    else:
        pytest.fail("unable to complete test without exceptions")
