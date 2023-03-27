import pytest
from tests.resources.test_support.controls import telescope_is_in_standby_state, telescope_is_in_on_state, telescope_is_in_off_state
from tests.resources.test_support.constant import (
    centralnode,
    csp_subarray1,
    csp_master,
    sdp_master,
    sdp_subarray1,
    tmc_subarraynode1,
    tmc_csp_master_leaf_node,
    tmc_csp_subarray_leaf_node,
    tmc_sdp_master_leaf_node,
    tmc_sdp_subarray_leaf_node,
    dish_master1
)
from tests.resources.test_support.common_utils.tmc_helpers import TmcHelper
from tests.conftest import LOGGER

@pytest.mark.SKA_mid
def test_telescope_on():
    """TelescopeOn() is executed."""
    try:
        fixture = {}
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
        fixture["state"] = "Unknown"

        """Verify Telescope is Off/Standby"""
        assert telescope_is_in_standby_state()
        LOGGER.info("Staring up the Telescope")

        """Invoke TelescopeOn() command on TMC"""
        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
        tmc_helper.set_to_on(sdp_subarray=sdp_subarray1,
                             csp_subarray=csp_subarray1,
                             csp_master=csp_master,
                             tmc_subarraynode=tmc_subarraynode1,
                             sdp_master=sdp_master,
                             dish_master=dish_master1
                             )
        LOGGER.info("TelescopeOn command is invoked successfully")

        """Verify State transitions after TelescopeOn"""
        assert telescope_is_in_on_state()
        fixture["state"] = "TelescopeOn"

        """Invoke TelescopeOff() command on TMC"""
        tmc_helper.set_to_off(sdp_subarray=sdp_subarray1,
                              csp_subarray=csp_subarray1,
                              csp_master=csp_master,
                              tmc_subarraynode=tmc_subarraynode1,
                              sdp_master=sdp_master,
                              dish_master=dish_master1
                             )

        """Verify State transitions after TelescopeOff"""
        assert telescope_is_in_off_state()
        fixture["state"] = "TelescopeOff"

        LOGGER.info("Tests complete.")

    except:
        LOGGER.info("Exception occurred in the test for state = {}".format(fixture["state"]))
        LOGGER.info("Tearing down...")
        if fixture["state"] == "TelescopeOn":
            tmc_helper.set_to_off(sdp_subarray=sdp_subarray1,
                                  csp_subarray=csp_subarray1,
                                  csp_master=csp_master,
                                  tmc_subarraynode=tmc_subarraynode1,
                                  sdp_master=sdp_master,
                                  dish_master=dish_master1
                                  )
        raise