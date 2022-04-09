import logging
import pytest
from tests.resources.test_support.controls import telescope_is_in_standby, telescope_is_in_on, telescope_is_in_off
import tests.resources.test_support.tmc_helpers as tmc

LOGGER = logging.getLogger(__name__)

@pytest.mark.SKA_mid
def test_telescope_standby():
    """TelescopeStandby() is executed."""
    try:
        fixture = {}
        fixture["state"] = "Unknown"

        """Verify Telescope is Off/Standby"""
        assert telescope_is_in_standby()
        LOGGER.info("Staring up the Telescope")

        """Invoke TelescopeOn() command on TMC"""
        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
        tmc.set_to_on()
        LOGGER.info("TelescopeOn command is invoked successfully")

        """Verify State transitions after TelescopeOn"""
        assert telescope_is_in_on()
        fixture["state"] = "TelescopeOn"

        """Invoke TelescopeOff() command on TMC"""
        tmc.set_to_standby()

        """Verify State transitions after TelescopeOff"""
        assert telescope_is_in_standby()
        fixture["state"] = "TelescopeOff"

        LOGGER.info("Tests complete: tearing down...")

    except:
        LOGGER.info("Tearing down failed test, state = {}".format(fixture["state"]))
        if fixture["state"] == "TelescopeOn":
            tmc.set_to_off()
        raise
