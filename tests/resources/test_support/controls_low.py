# local depencies
from tests.resources.test_support.helpers_low import (
    resource
)
from tests.conftest import LOGGER

# Tango device fqdns used across to create device proxy
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


    return (resource(sdp_subarray1).get("State") in ["DISABLE" , "OFF"],
    resource(sdp_master).get("State") in ["DISABLE", "STANDBY"],
    resource(csp_master).get("State") in ["DISABLE", "STANDBY"],
    resource(csp_subarray1).get("State") in ["DISABLE", "OFF"],
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
    ] == ["OFF", "OFF", "OFF", "OFF",]


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
