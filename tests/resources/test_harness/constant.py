"""Define Constants
"""
import numpy as np
from ska_control_model import ObsState

from tests.resources.test_harness.utils.enums import (
    FaultType,
    ResultCode,
    SimulatorDeviceType,
)

centralnode = "ska_mid/tm_central/central_node"
tmc_subarraynode1 = "ska_mid/tm_subarray_node/1"
tmc_subarraynode2 = "ska_mid/tm_subarray_node/2"
tmc_subarraynode3 = "ska_mid/tm_subarray_node/3"
tmc_csp_master_leaf_node = "ska_mid/tm_leaf_node/csp_master"
tmc_sdp_master_leaf_node = "ska_mid/tm_leaf_node/sdp_master"
tmc_csp_subarray_leaf_node = "ska_mid/tm_leaf_node/csp_subarray01"
tmc_sdp_subarray_leaf_node = "ska_mid/tm_leaf_node/sdp_subarray01"
tmc_dish_leaf_node1 = "ska_mid/tm_leaf_node/d0001"
tmc_dish_leaf_node2 = "ska_mid/tm_leaf_node/d0002"
sdp_subarray1 = "mid-sdp/subarray/01"
sdp_subarray2 = "mid-sdp/subarray/02"
sdp_subarray3 = "mid-sdp/subarray/03"
csp_subarray1 = "mid-csp/subarray/01"
csp_subarray2 = "mid-csp/subarray/02"
csp_subarray3 = "mid-csp/subarray/03"
sdp_master = "mid-sdp/control/0"
csp_master = "mid-csp/control/0"
dish_master1 = "ska001/elt/master"
dish_master2 = "ska002/elt/master"
dish_master3 = "ska003/elt/master"
dish_master4 = "ska004/elt/master"
sdp_queue_connector = "mid-sdp/queueconnector/01"


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

DEVICE_LIST_FOR_CHECK_DEVICES = [
    centralnode,
    csp_subarray1,
    sdp_subarray1,
    tmc_subarraynode1,
    tmc_csp_master_leaf_node,
    tmc_csp_subarray_leaf_node,
    tmc_sdp_master_leaf_node,
    tmc_sdp_subarray_leaf_node,
]

DEVICE_OBS_STATE_SCANNING_INFO = {
    sdp_subarray1: ["SCANNING"],
    tmc_subarraynode1: ["SCANNING"],
    csp_subarray1: ["SCANNING"],
}


INTERMEDIATE_STATE_DEFECT = {
    "enabled": True,
    "fault_type": FaultType.STUCK_IN_INTERMEDIATE_STATE,
    "error_message": "Device stuck in intermediate state",
    "result": ResultCode.FAILED,
    "intermediate_state": ObsState.RESOURCING,
}

OBS_STATE_RESOURCING_STUCK_DEFECT = {
    "enabled": True,
    "fault_type": FaultType.STUCK_IN_OBSTATE,
    "error_message": "Device stuck in Resourcing state",
    "result": ResultCode.FAILED,
    "intermediate_state": ObsState.RESOURCING,
}

INTERMEDIATE_OBSSTATE_EMPTY_DEFECT = {
    "enabled": True,
    "fault_type": FaultType.STUCK_IN_INTERMEDIATE_STATE,
    "error_message": "Device stuck in intermediate state",
    "result": ResultCode.FAILED,
    "intermediate_state": ObsState.EMPTY,
}

COMMAND_FAILED_WITH_EXCEPTION_OBSSTATE_EMPTY = {
    "enabled": True,
    "fault_type": FaultType.FAILED_RESULT,
    "error_message": "Default exception.",
    "result": ResultCode.FAILED,
    "target_obsstates": [ObsState.RESOURCING, ObsState.EMPTY],
}

POINTING_OFFSETS = np.array(
    [
        [
            "SKA001",
            -4.115211938625473,
            69.9725295732531,
            -7.090356031104502,
            104.10028693155607,
            70.1182176899719,
            78.8829949012184,
            95.49061976199042,
            729.5782881970024,
            119.27311545171803,
            1065.4074085647912,
            0.9948872678443994,
            0.8441090109163307,
        ],
        [
            "SKA002",
            -4.115211938625473,
            69.10028693155607,
            -7.5782881970024,
            104.10028693155607,
            70.1182176899719,
            78.8829949012184,
            95.49061976199042,
            729.5782881970024,
            119.27311545171803,
            1065.4074085647912,
            0.9948872678443994,
            0.8441090109163307,
        ],
    ]
)


low_centralnode = "ska_low/tm_central/central_node"
tmc_low_subarraynode1 = "ska_low/tm_subarray_node/1"
tmc_low_subarraynode2 = "ska_low/tm_subarray_node/2"
tmc_low_subarraynode3 = "ska_low/tm_subarray_node/3"
low_csp_master_leaf_node = "ska_low/tm_leaf_node/csp_master"
low_sdp_master_leaf_node = "ska_low/tm_leaf_node/sdp_master"
mccs_master_leaf_node = "ska_low/tm_leaf_node/mccs_master"
low_csp_subarray_leaf_node = "ska_low/tm_leaf_node/csp_subarray01"
low_sdp_subarray_leaf_node = "ska_low/tm_leaf_node/sdp_subarray01"
mccs_subarray_leaf_node = "ska_low/tm_leaf_node/mccs_subarray01"
low_sdp_subarray1 = "low-sdp/subarray/01"
low_sdp_subarray2 = "low-sdp/subarray/02"
low_sdp_subarray3 = "low-sdp/subarray/03"
low_csp_subarray1 = "low-csp/subarray/01"
low_csp_subarray2 = "low-csp/subarray/02"
low_csp_subarray3 = "low-csp/subarray/03"
low_sdp_master = "low-sdp/control/0"
low_csp_master = "low-csp/control/0"
mccs_controller = "low-mccs/control/control"
mccs_subarray1 = "low-mccs/subarray/01"
mccs_subarray2 = "low-mccs/subarray/02"
mccs_subarray3 = "low-mccs/subarray/03"
processor1 = "low-cbf/processor/0.0.0"

device_dict = {
    "csp_master": csp_master,
    "tmc_subarraynode": tmc_subarraynode1,
    "sdp_master": sdp_master,
    "dish_master1": dish_master1,
    "dish_master2": dish_master2,
    "sdp_subarray": sdp_subarray1,
    "csp_subarray": csp_subarray1,
    "sdp_subarray_leaf_node": tmc_sdp_subarray_leaf_node,
    "csp_subarray_leaf_node": tmc_csp_subarray_leaf_node,
}

device_dict_low = {
    "csp_master": low_csp_master,
    "tmc_subarraynode": tmc_low_subarraynode1,
    "sdp_master": low_sdp_master,
    "mccs_master": mccs_controller,
    "sdp_subarray": low_sdp_subarray1,
    "csp_subarray": low_csp_subarray1,
    "sdp_subarray_leaf_node": low_sdp_subarray_leaf_node,
    "csp_subarray_leaf_node": low_csp_subarray_leaf_node,
    "mccs_master_leaf_node": mccs_master_leaf_node,
}

SIMULATOR_DEVICE_FQDN_DICT = {
    SimulatorDeviceType.LOW_SDP_DEVICE: [low_sdp_subarray1],
    SimulatorDeviceType.LOW_CSP_DEVICE: [low_csp_subarray1],
    SimulatorDeviceType.LOW_SDP_MASTER_DEVICE: [low_sdp_master],
    SimulatorDeviceType.LOW_CSP_MASTER_DEVICE: [low_csp_master],
    SimulatorDeviceType.MCCS_MASTER_DEVICE: [mccs_controller],
    SimulatorDeviceType.MID_SDP_DEVICE: [sdp_subarray1],
    SimulatorDeviceType.MID_CSP_DEVICE: [csp_subarray1],
    SimulatorDeviceType.DISH_DEVICE: [dish_master1, dish_master2],
    SimulatorDeviceType.MID_SDP_MASTER_DEVICE: [sdp_master],
    SimulatorDeviceType.MID_CSP_MASTER_DEVICE: [csp_master],
    SimulatorDeviceType.MCCS_SUBARRAY_DEVICE: [mccs_subarray1],
}
