import pytest
from tests.resources.test_support.controls import telescope_is_in_standby_state, telescope_is_in_on_state, telescope_is_in_off_state
import tests.resources.test_support.tmc_helpers as tmc
from tests.conftest import LOGGER
from tests.resources.test_support.tmc_helpers import tear_down

@pytest.mark.SKA_mid
def test_telescope_standby():
    """TelescopeStandby() is executed."""
    try:
        """Verify Telescope is Off/Standby"""
        assert telescope_is_in_standby_state()
        LOGGER.info("Staring up the Telescope")

        """Invoke TelescopeOn() command on TMC"""
        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
        tmc.set_to_on()
        LOGGER.info("TelescopeOn command is invoked successfully")

        """Verify State transitions after TelescopeOn"""
        assert telescope_is_in_on_state()

        """Invoke TelescopeStandby() command on TMC"""
        tmc.set_to_standby()

        """Verify State transitions after TelescopeStandby"""
        assert telescope_is_in_standby_state()

        LOGGER.info("Tests complete.")

    except Exception:
        tear_down()
