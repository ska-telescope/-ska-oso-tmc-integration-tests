centralnode = "ska_low/tm_central/central_node"
tmc_subarraynode1 = "ska_low/tm_subarray_node/1"
tmc_subarraynode2 = "ska_low/tm_subarray_node/2"
tmc_subarraynode3 = "ska_low/tm_subarray_node/3"
tmc_csp_master_leaf_node = "ska_low/tm_leaf_node/csp_master"
tmc_sdp_master_leaf_node = "ska_low/tm_leaf_node/sdp_master"
tmc_csp_subarray_leaf_node= "ska_low/tm_leaf_node/csp_subarray01"
tmc_sdp_subarray_leaf_node= "ska_low/tm_leaf_node/sdp_subarray01"
sdp_subarray1 = "low-sdp/subarray/01"
sdp_subarray2 = "low-sdp/subarray/02"
sdp_subarray3 = "low-sdp/subarray/03"
csp_subarray1 = "low-csp/subarray/01"
csp_subarray2 = "low-csp/subarray/02"
csp_subarray3 = "low-csp/subarray/03"
sdp_master = "low-sdp/control/0"
csp_master = "low-csp/control/0"

DEVICE_STATE_STANDBY_INFO = {
    sdp_subarray1: ["DISABLE" , "OFF"],
    sdp_master: ["DISABLE", "STANDBY", "OFF"],
    csp_master: ["DISABLE", "STANDBY", "OFF"],
    csp_subarray1: ["DISABLE", "OFF"]
}

DEVICE_STATE_ON_INFO = {
    sdp_subarray1: ["ON"],
    sdp_master: ["ON"],
    csp_master: ["ON"],
    csp_subarray1: ["ON"],
    centralnode: ["ON"]
}

DEVICE_STATE_OFF_INFO = {
    sdp_subarray1: ["OFF"],
    sdp_master: ["OFF"],
    csp_master: ["OFF"],
    csp_subarray1: ["OFF"]
}

DEVICE_OBS_STATE_IDLE_INFO = {
    sdp_subarray1: ["IDLE"],
    tmc_subarraynode1: ["IDLE"],
    csp_subarray1: ["IDLE"]
}

DEVICE_OBS_STATE_EMPTY_INFO = {
    sdp_subarray1: ["EMPTY"],
    tmc_subarraynode1: ["EMPTY"],
    csp_subarray1: ["EMPTY"] 
}

DEVICE_OBS_STATE_READY_INFO = {
    sdp_subarray1: ["READY"],
    tmc_subarraynode1: ["READY"],
    csp_subarray1: ["READY"]
}

DEVICE_OBS_STATE_SCANNING_INFO = {
    sdp_subarray1: ["SCANNING"],
    tmc_subarraynode1: ["SCANNING"],
    csp_subarray1: ["SCANNING"]
}

DEVICE_OBS_STATE_ABORT_INFO = {
    sdp_subarray1: ["ABORTED"],
    tmc_subarraynode1: ["ABORTED"],
    csp_subarray1: ["ABORTED"]
}

DEVICE_HEALTH_STATE_OK_INFO = {
    tmc_csp_subarray_leaf_node: "OK",
    centralnode: "OK",
    tmc_csp_master_leaf_node: "OK",
    tmc_sdp_master_leaf_node: "OK",
    tmc_sdp_subarray_leaf_node: "OK"
}

ON_OFF_DEVICE_COMMAND_DICT = {
    "sdp_subarray": sdp_subarray1, #TODO use this as as list when multiple subarray considered in testing
    "csp_subarray": csp_subarray1,
    "csp_master": csp_master,
    "tmc_subarraynode": tmc_subarraynode1,
    "sdp_master": sdp_master,
    "centralnode": centralnode 
}


DEVICE_LIST_FOR_CHECK_DEVICES=[
    centralnode,
    csp_subarray1,
    sdp_subarray1,
    tmc_subarraynode1,
    tmc_csp_master_leaf_node,
    tmc_csp_subarray_leaf_node,
    tmc_sdp_master_leaf_node,
    tmc_sdp_subarray_leaf_node
    ]