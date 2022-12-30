# local depencies
from tests.resources.test_support.helpers import (
    resource
)
import os
from tests.conftest import LOGGER, TELESCOPE_ENV

# Tango device fqdns used across to create device proxy

dish_master1 = "mid_d0001/elt/master"
dish_master2 = "mid_d0002/elt/master"
dish_master3 = "mid_d0003/elt/master"
dish_master4 = "mid_d0004/elt/master"

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
    
def validate_states(device_info, attr):
    """_summary_

    Args:
        device_info (_type_): _description_
    """
    device_names = device_info.keys()
    state_validations = []
    for dev_name in device_names:
        LOGGER.info(f'resource.get("{attr}")' + str(resource(dev_name).get(attr)))
        state_to_check = device_info[dev_name]
        state_validations.append(
            resource(dev_name).get(attr) in state_to_check
        )
    return state_to_check


def telescope_is_in_standby_state():
    device_info = {
        sdp_master: ["DISABLE", "STANDBY"],
        sdp_subarray1: ["DISABLE" , "OFF"], 
        csp_master: ["DISABLE", "STANDBY"], 
        csp_subarray1: ["DISABLE", "OFF"]
    }
    if TELESCOPE_ENV == "SKA-mid":
        device_info[dish_master1] = ["DISABLE", "OFF"]
    
    return validate_states(device_info, "State")
#     LOGGER.info(
#         'resource(sdp_master).get("State")'
#         + str(resource(sdp_master).get("State"))
#     )
#     LOGGER.info(
#         'resource(sdp_subarray1).get("State")'
#         + str(resource(sdp_subarray1).get("State"))
#     )
#     LOGGER.info(
#         'resource(csp_master).get("State")'
#         + str(resource(csp_master).get("State"))
#     )
#     LOGGER.info(
#         'resource(csp_subarray1).get("State")'
#         + str(resource(csp_subarray1).get("State"))
#     )
#     LOGGER.info(
#         'resource(dish_master1).get("State")'
#         + str(resource(dish_master1).get("State"))
#     )

#     return (resource(sdp_subarray1).get("State") in ["DISABLE" , "OFF"],
#     resource(sdp_master).get("State") in ["DISABLE", "STANDBY"],
#     resource(csp_master).get("State") in ["DISABLE", "STANDBY"],
#     resource(csp_subarray1).get("State") in ["DISABLE", "OFF"],
#     resource(dish_master1).get("State") in ["DISABLE", "OFF"],
# )

def telescope_is_in_on_state():
    LOGGER.info(
        'resource(tmc_subarraynode1).get("State")'
        + str(resource(tmc_subarraynode1).get("State"))
    )
    device_info = {
        sdp_master: ["ON"],
        sdp_subarray1: ["ON"], 
        csp_master: ["ON"], 
        csp_subarray1: ["ON"],
        centralnode: ["ON"]
    }
    if TELESCOPE_ENV == "SKA-mid":
        device_info[dish_master1] = ["ON"]
    
    return validate_states(device_info, "State")
    # LOGGER.info(
    #     'resource(sdp_master).get("State")'
    #     + str(resource(sdp_master).get("State"))
    # )
    # LOGGER.info(
    #     'resource(sdp_subarray1).get("State")'
    #     + str(resource(sdp_subarray1).get("State"))
    # )
    # LOGGER.info(
    #     'resource(csp_master).get("State")'
    #     + str(resource(csp_master).get("State"))
    # )
    # LOGGER.info(
    #     'resource(csp_subarray1).get("State")'
    #     + str(resource(csp_subarray1).get("State"))
    # )
    # LOGGER.info(
    #     'resource(dish_master1).get("State")'
    #     + str(resource(dish_master1).get("State"))
    # )
    # LOGGER.info(
    #     'resource(centralnode).get("State")'
    #     + str(resource(centralnode).get("State"))
    # )

    # return [
    #     resource(sdp_subarray1).get("State"),
    #     resource(sdp_master).get("State"),
    #     resource(csp_master).get("State"),
    #     resource(csp_subarray1).get("State"),
    #     resource(dish_master1).get("State"),
    #     resource(centralnode).get("State"),
    # ] == ["ON", "ON", "ON", "ON", "ON", "ON"]


def telescope_is_in_off_state():
    LOGGER.info(
        'resource(sdp_master).get("State")'
        + str(resource(sdp_master).get("State"))
    )
    LOGGER.info(
        'resource(sdp_subarray1).get("State")'
        + str(resource(sdp_subarray1).get("State"))
    )
    LOGGER.info(
        'resource(csp_master).get("State")'
        + str(resource(csp_master).get("State"))
    )
    LOGGER.info(
        'resource(csp_subarray1).get("State")'
        + str(resource(csp_subarray1).get("State"))
    )
    LOGGER.info(
        'resource(dish_master1).get("State")'
        + str(resource(dish_master1).get("State"))
    )

    return [
        resource(sdp_subarray1).get("State"),
        resource(sdp_master).get("State"),
        resource(csp_master).get("State"),
        resource(csp_subarray1).get("State"),
        resource(dish_master1).get("State"),
    ] == ["OFF", "OFF", "OFF", "OFF", "STANDBY"]


def subarray_obs_state_is_idle():
   LOGGER.info(
        'resource(tmc_subarraynode1).get("obsState")'
         + str(resource(tmc_subarraynode1).get("obsState"))
    )
   LOGGER.info(
        'resource(sdp_subarray1).get("obsState")'
         + str(resource(sdp_subarray1).get("obsState"))
    )
   LOGGER.info(
        'resource(csp_subarray1).get("obsState")'
         + str(resource(csp_subarray1).get("obsState"))
    )

   return [
        resource(sdp_subarray1).get("obsState"),
        resource(tmc_subarraynode1).get("obsState"),
        resource(csp_subarray1).get("obsState"),
    ] == ["IDLE", "IDLE", "IDLE",]


def subarray_obs_state_is_empty():
   LOGGER.info(
        'resource(tmc_subarraynode1).get("obsState")'
         + str(resource(tmc_subarraynode1).get("obsState"))
    )
   LOGGER.info(
        'resource(sdp_subarray1).get("obsState")'
         + str(resource(sdp_subarray1).get("obsState"))
    )
   LOGGER.info(
        'resource(csp_subarray1).get("obsState")'
         + str(resource(csp_subarray1).get("obsState"))
    )

   return [
        resource(sdp_subarray1).get("obsState"),
        resource(tmc_subarraynode1).get("obsState"),
        resource(csp_subarray1).get("obsState"),
    ] == ["EMPTY", "EMPTY", "EMPTY",]


def subarray_obs_state_is_ready():
   LOGGER.info(
        'resource(tmc_subarraynode1).get("obsState")'
         + str(resource(tmc_subarraynode1).get("obsState"))
    )
   LOGGER.info(
        'resource(sdp_subarray1).get("obsState")'
         + str(resource(sdp_subarray1).get("obsState"))
    )
   LOGGER.info(
        'resource(csp_subarray1).get("obsState")'
         + str(resource(csp_subarray1).get("obsState"))
    )

   return [
        resource(sdp_subarray1).get("obsState"),
        resource(tmc_subarraynode1).get("obsState"),
        resource(csp_subarray1).get("obsState"),
    ] == ["READY", "READY", "READY",]
