import pytest
from tests.resources.test_support.low.controls import telescope_is_in_standby_state, telescope_is_in_on_state, telescope_is_in_off_state
import tests.resources.test_support.low.tmc_helpers as tmc
from tests.conftest import LOGGER
from tango import DeviceProxy
@pytest.mark.SKA_low
def test_telescope_on():

    """Tests whether the Central Node Low is up."""
    proxy = DeviceProxy("ska_low/tm_central/central_node")
    result = proxy.ping()
    assert result > 1

    # """TelescopeOn() is executed."""
    # try:
    #     fixture = {}
    #     fixture["state"] = "Unknown"

    #     """Verify Telescope is Off/Standby"""
    #     assert telescope_is_in_standby_state()
    #     LOGGER.info("Staring up the Telescope")

    #     """Invoke TelescopeOn() command on TMC"""
    #     LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
    #     tmc.set_to_on()
    #     LOGGER.info("TelescopeOn command is invoked successfully")

    #     """Verify State transitions after TelescopeOn"""
    #     assert telescope_is_in_on_state()
    #     fixture["state"] = "TelescopeOn"

    #     """Invoke TelescopeOff() command on TMC"""
    #     tmc.set_to_off()

    #     """Verify State transitions after TelescopeOff"""
    #     assert telescope_is_in_off_state()
    #     fixture["state"] = "TelescopeOff"

    #     LOGGER.info("Tests complete.")

    # except:
    #     LOGGER.info("Exception occurred in the test for state = {}".format(fixture["state"]))
    #     LOGGER.info("Tearing down...")
    #     if fixture["state"] == "TelescopeOn":
    #         tmc.set_to_off()
    #     raise
