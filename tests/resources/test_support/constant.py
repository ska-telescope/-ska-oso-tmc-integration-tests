centralnode = "ska_mid/tm_central/central_node"
tmc_subarraynode1 = "ska_mid/tm_subarray_node/1"
tmc_subarraynode2 = "ska_mid/tm_subarray_node/2"
tmc_subarraynode3 = "ska_mid/tm_subarray_node/3"
tmc_csp_master_leaf_node = "ska_mid/tm_leaf_node/csp_master"
tmc_sdp_master_leaf_node = "ska_mid/tm_leaf_node/sdp_master"
tmc_csp_subarray_leaf_node = "ska_mid/tm_leaf_node/csp_subarray01"
tmc_sdp_subarray_leaf_node = "ska_mid/tm_leaf_node/sdp_subarray01"
sdp_subarray1 = "mid-sdp/subarray/01"
sdp_subarray2 = "mid-sdp/subarray/02"
sdp_subarray3 = "mid-sdp/subarray/03"
csp_subarray1 = "mid-csp/subarray/01"
csp_subarray2 = "mid-csp/subarray/02"
csp_subarray3 = "mid-csp/subarray/03"
sdp_master = "mid-sdp/control/0"
csp_master = "mid-csp/control/0"
dish_master1 = "ska001/dish/master"
dish_master2 = "ska002/dish/master"
dish_master3 = "ska003/dish/master"
dish_master4 = "ska004/dish/master"


DEVICE_HEALTH_STATE_OK_INFO = {
    tmc_csp_subarray_leaf_node: "OK",
    centralnode: "OK",
    tmc_csp_master_leaf_node: "OK",
    tmc_sdp_master_leaf_node: "OK",
    tmc_sdp_subarray_leaf_node: "OK",
}

# TODO use this as as list when multiple subarray considered in testing
ON_OFF_DEVICE_COMMAND_DICT = {
    "sdp_subarray": sdp_subarray1,
    "csp_subarray": csp_subarray1,
    "csp_master": csp_master,
    "tmc_subarraynode": tmc_subarraynode1,
    "sdp_master": sdp_master,
    "dish_master": dish_master1,
    "central_node": centralnode,
}

DEVICE_STATE_STANDBY_INFO = {
    sdp_subarray1: ["DISABLE", "OFF"],
    sdp_master: ["DISABLE", "STANDBY", "OFF"],
    csp_master: ["DISABLE", "STANDBY", "OFF"],
    csp_subarray1: ["DISABLE", "OFF"],
    dish_master1: ["DISABLE", "STANDBY"],
}

DEVICE_STATE_ON_INFO = {
    sdp_subarray1: ["ON"],
    sdp_master: ["ON"],
    csp_master: ["ON"],
    csp_subarray1: ["ON"],
    centralnode: ["ON"],
    dish_master1: ["STANDBY"],
}

DEVICE_OBS_STATE_EMPTY_INFO = {
    sdp_subarray1: ["EMPTY"],
    tmc_subarraynode1: ["EMPTY"],
    csp_subarray1: ["EMPTY"],
}

DEVICE_OBS_STATE_READY_INFO = {
    sdp_subarray1: ["READY"],
    tmc_subarraynode1: ["READY"],
    csp_subarray1: ["READY"],
}

DEVICE_OBS_STATE_IDLE_INFO = {
    sdp_subarray1: ["IDLE"],
    tmc_subarraynode1: ["IDLE"],
    csp_subarray1: ["IDLE"],
}

DEVICE_STATE_OFF_INFO = {
    sdp_subarray1: ["OFF"],
    sdp_master: ["OFF"],
    csp_master: ["OFF"],
    csp_subarray1: ["OFF"],
    dish_master1: ["STANDBY"],
}

DEVICE_OBS_STATE_ABORT_INFO = {
    sdp_subarray1: ["ABORTED"],
    tmc_subarraynode1: ["ABORTED"],
    csp_subarray1: ["ABORTED"],
}
