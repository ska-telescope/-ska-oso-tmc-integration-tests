import pytest

from tests.conftest import LOGGER
from tests.resources.test_support.common_utils.telescope_controls import (
    BaseTelescopeControl,
)
from tests.resources.test_support.common_utils.tmc_helpers import (
    TmcHelper,
    tear_down,
)
from tests.resources.test_support.constant import (
    DEVICE_STATE_ON_INFO,
    DEVICE_STATE_STANDBY_INFO,
    ON_OFF_DEVICE_COMMAND_DICT,
    centralnode,
    tmc_subarraynode1,
)


@pytest.mark.SKA_mid
def test_telescope_standby():
    """TelescopeStandby() is executed."""
    try:
        telescope_control = BaseTelescopeControl()
        tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)
        # Verify Telescope is Off/Standby
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )
        LOGGER.info("Starting up the Telescope")

        # Invoke TelescopeOn() command on TMC
        tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)
        LOGGER.info("TelescopeOn command is invoked successfully")

        # Verify State transitions after TelescopeOn
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_ON_INFO, "State"
        )

        # Invoke TelescopeStandby() command on TMC
        tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)

        # Checking the availability of Telescope
        tmc_helper.check_telescope_availability()

        # Verify State transitions after TelescopeStandby
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )

        LOGGER.info("Tests complete.")

    except Exception as e:
        LOGGER.info("In tear down. \nThe Exception is %s", e)
        tear_down(**ON_OFF_DEVICE_COMMAND_DICT)
