# local depencies
from tests.resources.test_support.low.helpers import (
    resource
)
import os
from tests.conftest import LOGGER
from tests.resources.test_support.constant_low import *

# Tango device fqdns used across to create device proxy
    
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
    # device_info = {
    #     sdp_master: ["DISABLE", "STANDBY"],
    #     sdp_subarray1: ["DISABLE" , "OFF"], 
    #     csp_master: ["DISABLE", "STANDBY"], 
    #     csp_subarray1: ["DISABLE", "OFF"]
    # }
    # if TELESCOPE_ENV == "SKA-mid":
    #     device_info[dish_master1] = ["DISABLE", "OFF"]
    
    # return validate_states(device_info, "State")
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

    return (
        resource(sdp_subarray1).get("State") in ["DISABLE" , "OFF"],
        resource(sdp_master).get("State") in ["DISABLE", "STANDBY"],
        resource(csp_master).get("State") in ["DISABLE", "STANDBY"],
        resource(csp_subarray1).get("State") in ["DISABLE", "OFF"]
    )

def telescope_is_in_on_state():
    LOGGER.info(
        'resource(tmc_subarraynode1).get("State")'
        + str(resource(tmc_subarraynode1).get("State"))
    )
    # device_info = {
    #     sdp_master: ["ON"],
    #     sdp_subarray1: ["ON"], 
    #     csp_master: ["ON"], 
    #     csp_subarray1: ["ON"],
    #     centralnode: ["ON"]
    # }
    # if TELESCOPE_ENV == "SKA-mid":
    #     device_info[dish_master1] = ["ON"]
    
    # return validate_states(device_info, "State")
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
        'resource(centralnode).get("State")'
        + str(resource(centralnode).get("State"))
    )

    return [
        resource(sdp_subarray1).get("State"),
        resource(sdp_master).get("State"),
        resource(csp_master).get("State"),
        resource(csp_subarray1).get("State"),
        resource(centralnode).get("State"),
    ] == ["ON", "ON", "ON", "ON", "ON"]


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
    return [
        resource(sdp_subarray1).get("State"),
        resource(sdp_master).get("State"),
        resource(csp_master).get("State"),
        resource(csp_subarray1).get("State"),
    ] == ["OFF", "OFF", "OFF", "OFF"]


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
