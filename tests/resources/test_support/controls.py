# local depencies
from tests.resources.test_support.helpers import (
    resource
)
import os
from tests.conftest import LOGGER, TELESCOPE_ENV
from tests.resources.test_support.constant import *

# Tango device fqdns used across to create device proxy


def telescope_is_in_standby_state():
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

    return (
        resource(sdp_subarray1).get("State") in ["DISABLE" , "OFF"],
        resource(sdp_master).get("State") in ["DISABLE", "STANDBY"],
        resource(csp_master).get("State") in ["DISABLE", "STANDBY"],
        resource(csp_subarray1).get("State") in ["DISABLE", "OFF"],
        resource(dish_master1).get("State") in ["DISABLE", "OFF"],
    )

def telescope_is_in_on_state():
    LOGGER.info(
        'resource(tmc_subarraynode1).get("State")'
        + str(resource(tmc_subarraynode1).get("State"))
    )
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
    LOGGER.info(
        'resource(centralnode).get("State")'
        + str(resource(centralnode).get("State"))
    )

    return [
        resource(sdp_subarray1).get("State"),
        resource(sdp_master).get("State"),
        resource(csp_master).get("State"),
        resource(csp_subarray1).get("State"),
        resource(dish_master1).get("State"),
        resource(centralnode).get("State"),
    ] == ["ON", "ON", "ON", "ON", "ON", "ON"]


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