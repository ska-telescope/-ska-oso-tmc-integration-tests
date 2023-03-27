import pytest
from tests.resources.test_support.controls import telescope_is_in_standby_state, telescope_is_in_on_state, telescope_is_in_off_state
from tests.resources.test_support.constant import ON_OFF_DEVICE_COMMAND_DICT, centralnode
from tests.resources.test_support.common_utils.tmc_helpers import TmcHelper
from tests.conftest import LOGGER

@pytest.mark.SKA_mid
def test_telescope_on():
    """TelescopeOn() is executed."""
    try:
        fixture = {}
        tmc_helper = TmcHelper(centralnode)
        fixture["state"] = "Unknown"

        """Verify Telescope is Off/Standby"""
        assert telescope_is_in_standby_state()
        LOGGER.info("Starting up the Telescope")

        """Invoke TelescopeOn() command on TMC"""
        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
        tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)
        LOGGER.info("TelescopeOn command is invoked successfully")

        """Verify State transitions after TelescopeOn"""
        assert telescope_is_in_on_state()
        fixture["state"] = "TelescopeOn"

        """Invoke TelescopeOff() command on TMC"""
        tmc_helper.set_to_off(**ON_OFF_DEVICE_COMMAND_DICT)

        """Verify State transitions after TelescopeOff"""
        assert telescope_is_in_off_state()
        fixture["state"] = "TelescopeOff"

        LOGGER.info("Tests complete.")

    except:
        LOGGER.info("Exception occurred in the test for state = {}".format(fixture["state"]))
        LOGGER.info("Tearing down...")
        if fixture["state"] == "TelescopeOn":
            tmc_helper.set_to_off(**ON_OFF_DEVICE_COMMAND_DICT)
        raise