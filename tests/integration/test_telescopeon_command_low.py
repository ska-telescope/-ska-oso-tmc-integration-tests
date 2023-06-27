import pytest

from tests.conftest import LOGGER
from tests.resources.test_support.common_utils.tmc_helpers import TmcHelper
from tests.resources.test_support.constant_low import (
    DEVICE_STATE_OFF_INFO,
    DEVICE_STATE_ON_INFO,
    DEVICE_STATE_STANDBY_INFO,
    ON_OFF_DEVICE_COMMAND_DICT,
    centralnode,
    tmc_subarraynode1,
)
from tests.resources.test_support.low.telescope_controls_low import (
    TelescopeControlLow,
)


@pytest.mark.SKA_low
def test_telescope_on():
    """TelescopeOn() is executed."""
    try:
        telescope_control = TelescopeControlLow()
        tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)
        fixture = {}
        fixture["state"] = "Unknown"

        # Verify Telescope is Off/Standby
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )
        LOGGER.info("Starting up the Telescope")

        # # Invoke TelescopeOn() command on TMC
        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")

        tmc_helper.check_telescope_availability()
        tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)
        LOGGER.info("TelescopeOn command is invoked successfully")

        # # Verify State transitions after TelescopeOn
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_ON_INFO, "State"
        )
        fixture["state"] = "TelescopeOn"

        tmc_helper.check_telescope_availability()
        # # Invoke TelescopeOff() command on TMC
        tmc_helper.set_to_off(**ON_OFF_DEVICE_COMMAND_DICT)

        LOGGER.info("TelescopeOff command is invoked successfully")

        # # Verify State transitions after TelescopeOff
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_OFF_INFO, "State"
        )
        fixture["state"] = "TelescopeOff"

        LOGGER.info("test_telescope_on Tests complete.")

    except Exception:
        LOGGER.info(
            "Exception occurred in the test for state = {}".format(
                fixture["state"]
            )
        )
        LOGGER.info("Tearing Down test case")
        if fixture["state"] == "TelescopeOn":
            tmc_helper.set_to_off(**ON_OFF_DEVICE_COMMAND_DICT)
        raise
