import pytest
import tests.resources.test_support.low.tmc_helpers as tmc
from tests.resources.test_support.constant_low import DEVICE_STATE_STANDBY_INFO, DEVICE_STATE_ON_INFO, DEVICE_STATE_OFF_INFO
from tests.resources.test_support.low.telescope_controls_low import TelescopeControlLow
from tests.conftest import LOGGER

@pytest.mark.SKA_low_skip
def test_telescope_on():
    """TelescopeOn() is executed."""
    try:
        telescope_control = TelescopeControlLow()
        fixture = {}
        fixture["state"] = "Unknown"

        """Verify Telescope is Off/Standby"""
        assert telescope_control.is_in_valid_state(DEVICE_STATE_STANDBY_INFO, "State")
        LOGGER.info("Staring up the Telescope")

        """Invoke TelescopeOn() command on TMC"""
        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
        tmc.set_to_on()
        LOGGER.info("TelescopeOn command is invoked successfully")

        """Verify State transitions after TelescopeOn"""
        assert telescope_control.is_in_valid_state(DEVICE_STATE_ON_INFO, "State")
        fixture["state"] = "TelescopeOn"

        """Invoke TelescopeOff() command on TMC"""
        tmc.set_to_off()

        """Verify State transitions after TelescopeOff"""
        assert telescope_control.is_in_valid_state(DEVICE_STATE_OFF_INFO, "State")
        fixture["state"] = "TelescopeOff"

        LOGGER.info("Tests complete.")

    except:
        LOGGER.info("Exception occurred in the test for state = {}".format(fixture["state"]))
        LOGGER.info("Tearing down...")
        if fixture["state"] == "TelescopeOn":
            tmc.set_to_off()
        raise
