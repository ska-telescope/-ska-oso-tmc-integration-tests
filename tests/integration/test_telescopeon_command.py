import pytest

from tests.conftest import LOGGER
from tests.resources.test_support.common_utils.tmc_helpers import TmcHelper
from tests.resources.test_support.constant import (
    ON_OFF_DEVICE_COMMAND_DICT,
    centralnode,
    tmc_subarraynode1,
)
from tests.resources.test_support.controls import (
    telescope_is_in_off_state,
    telescope_is_in_on_state,
    telescope_is_in_standby_state,
)
from tests.resources.test_support.tmc_helpers import tear_down


@pytest.mark.SKA_mid
def test_telescope_on():
    """TelescopeOn() is executed."""
    try:
        tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)

        """Verify Telescope is Off/Standby"""
        assert telescope_is_in_standby_state()
        LOGGER.info("Starting up the Telescope")

        """Invoke TelescopeOn() command on TMC"""
        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
        tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)
        LOGGER.info("TelescopeOn command is invoked successfully")

        """Verify State transitions after TelescopeOn"""
        assert telescope_is_in_on_state()

        """Invoke TelescopeStandby() command on TMC"""
        tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)

        """Verify State transitions after TelescopeStandby"""
        assert telescope_is_in_standby_state()

        LOGGER.info("Tests complete.")

    except Exception:
        tear_down()
