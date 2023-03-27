import pytest
import tests.resources.test_support.low.tmc_helpers as tmc
from tests.resources.test_support.constant_low import (
    DEVICE_STATE_STANDBY_INFO,
    DEVICE_STATE_ON_INFO,
    DEVICE_STATE_OFF_INFO,
    centralnode,
    csp_subarray1,
    csp_master,
    sdp_master,
    sdp_subarray1,
    tmc_subarraynode1,
    tmc_csp_master_leaf_node,
    tmc_csp_subarray_leaf_node,
    tmc_sdp_master_leaf_node,
    tmc_sdp_subarray_leaf_node
)
from tests.resources.test_support.low.telescope_controls_low import TelescopeControlLow
from tests.conftest import LOGGER
from tests.resources.test_support.common_utils.tmc_helpers import TmcHelper


@pytest.mark.SKA_low
def test_telescope_on():
    """TelescopeOn() is executed."""
    try:
        telescope_control = TelescopeControlLow()
        tmc_helper = TmcHelper(
            centralnode,
            check_device_list=[
                centralnode,
                csp_subarray1,
                sdp_subarray1,
                tmc_subarraynode1,
                tmc_csp_master_leaf_node,
                tmc_csp_subarray_leaf_node,
                tmc_sdp_master_leaf_node,
                tmc_sdp_subarray_leaf_node
                ]
            )
        fixture = {}
        fixture["state"] = "Unknown"

        """Verify Telescope is Off/Standby"""
        assert telescope_control.is_in_valid_state(DEVICE_STATE_STANDBY_INFO, "State")
        LOGGER.info("Starting up the Telescope")

        """Invoke TelescopeOn() command on TMC"""
        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
        
        tmc_helper.set_to_on(sdp_subarray=sdp_subarray1,
                             csp_subarray=csp_subarray1,
                             csp_master=csp_master,
                             tmc_subarraynode=tmc_subarraynode1,
                             sdp_master=sdp_master
                             )
        LOGGER.info("TelescopeOn command is invoked successfully")

        """Verify State transitions after TelescopeOn"""
        assert telescope_control.is_in_valid_state(DEVICE_STATE_ON_INFO, "State")
        fixture["state"] = "TelescopeOn"

        """Invoke TelescopeOff() command on TMC"""
        tmc_helper.set_to_off(sdp_subarray=sdp_subarray1,
                              csp_subarray=csp_subarray1,
                              csp_master=csp_master,
                              tmc_subarraynode=tmc_subarraynode1,
                              sdp_master=sdp_master
                             )
        
        LOGGER.info("TelescopeOff command is invoked successfully")

        """Verify State transitions after TelescopeOff"""
        assert telescope_control.is_in_valid_state(DEVICE_STATE_OFF_INFO, "State")
        fixture["state"] = "TelescopeOff"

        LOGGER.info("test_telescope_on Tests complete.")

    except:
        LOGGER.info("Exception occurred in the test for state = {}".format(fixture["state"]))
        LOGGER.info("Tearing down the Telescope")
        if fixture["state"] == "TelescopeOn":
            tmc_helper.set_to_off(sdp_subarray=sdp_subarray1,
                                  csp_subarray=csp_subarray1,
                                  csp_master=csp_master,
                                  tmc_subarraynode=tmc_subarraynode1,
                                  sdp_master=sdp_master
                                  )
        raise
