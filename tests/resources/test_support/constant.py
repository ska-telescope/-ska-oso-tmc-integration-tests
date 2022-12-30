from tests.conftest import LOGGER, TELESCOPE_ENV

dish_master1 = "mid_d0001/elt/master"
dish_master2 = "mid_d0002/elt/master"
dish_master3 = "mid_d0003/elt/master"
dish_master4 = "mid_d0004/elt/master"

print(f"{TELESCOPE_ENV} is env")

if TELESCOPE_ENV == "SKA-low":
    centralnode = "ska_low/tm_central/central_node"
    tmc_subarraynode1 = "ska_low/tm_subarray_node/1"
    tmc_subarraynode2 = "ska_low/tm_subarray_node/2"
    tmc_subarraynode3 = "ska_low/tm_subarray_node/3"
    sdp_subarray1 = "low-sdp/subarray/01"
    sdp_subarray2 = "low-sdp/subarray/02"
    sdp_subarray3 = "low-sdp/subarray/03"
    csp_subarray1 = "low-csp/subarray/01"
    csp_subarray2 = "low-csp/subarray/02"
    csp_subarray3 = "low-csp/subarray/03"
    sdp_master = "low-sdp/control/0"
    csp_master = "low-csp/control/0"
else:
    centralnode = "ska_mid/tm_central/central_node"
    tmc_subarraynode1 = "ska_mid/tm_subarray_node/1"
    tmc_subarraynode2 = "ska_mid/tm_subarray_node/2"
    tmc_subarraynode3 = "ska_mid/tm_subarray_node/3"
    sdp_subarray1 = "mid-sdp/subarray/01"
    sdp_subarray2 = "mid-sdp/subarray/02"
    sdp_subarray3 = "mid-sdp/subarray/03"
    csp_subarray1 = "mid-csp/subarray/01"
    csp_subarray2 = "mid-csp/subarray/02"
    csp_subarray3 = "mid-csp/subarray/03"
    sdp_master = "mid-sdp/control/0"
    csp_master = "mid-csp/control/0"
    dish_master1 = "mid_d0001/elt/master"
    dish_master2 = "mid_d0002/elt/master"
    dish_master3 = "mid_d0003/elt/master"
    dish_master4 = "mid_d0004/elt/master"