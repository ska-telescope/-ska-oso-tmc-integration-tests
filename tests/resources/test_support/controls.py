# local depencies
from tests.resources.test_support.helpers import (
    resource
)
from tests.conftest import LOGGER

centralnode = "ska_mid/tm_central/central_node"
tm_subarraynode1 = "ska_mid/tm_subarray_node/1"
sdp_subarray1 = "mid_sdp/elt/subarray_1"
csp_subarray1 = "mid_csp/elt/subarray_01"
sdp_master = "mid_sdp/elt/master"
csp_master = "mid_csp/elt/master"
dish_master1 = "mid_d0001/elt/master"


def telescope_is_in_standby_state():
    LOGGER.info(
        'resource(tm_subarraynode1).get("State")'
        + str(resource(tm_subarraynode1).get("State"))
    )
    LOGGER.info(
        'resource(sdp_master_fqdn).get("State")'
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
    return (resource(sdp_subarray1).get("State") in ["DISABLE" , "OFF"],
    resource(sdp_master).get("State") in ["DISABLE", "STANDBY"],
    resource(csp_master).get("State") in ["DISABLE", "STANDBY"],
    resource(csp_subarray1).get("State") in ["DISABLE", "OFF"],
    resource(dish_master1).get("State") in ["DISABLE", "OFF"],
)

def telescope_is_in_on_state():
    LOGGER.info(
        'resource(tm_subarraynode1).get("State")'
        + str(resource(tm_subarraynode1).get("State"))
    )
    LOGGER.info(
        'resource(sdp_master_fqdn).get("State")'
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
    LOGGER.info(
        'resource(centralnode).get("telescopeState")'
        + str(resource(centralnode).get("telescopeState")))

    return [
        resource(sdp_subarray1).get("State"),
        resource(sdp_master).get("State"),
        resource(csp_master).get("State"),
        resource(csp_subarray1).get("State"),
        resource(dish_master1).get("State"),
        resource(centralnode).get("State"),
        resource(centralnode).get("telescopeState"),
    ] == ["ON", "ON", "ON", "ON", "ON", "ON", "ON"]


def telescope_is_in_off_state():
    LOGGER.info(
        'resource(tm_subarraynode1).get("State")'
        + str(resource(tm_subarraynode1).get("State"))
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
        'resource(centralnode).get("State")'
        + str(resource(centralnode).get("State")))

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
        resource(centralnode).get("State"),
        resource(centralnode).get("telescopeState"),
    ] == ["OFF", "OFF", "STANDBY", "OFF", "OFF", "ON", "STANDBY"]


def subarray_obs_state_is_idle ():
   LOGGER.info(
        'resource(tm_subarraynode1).get("obsState")'
         + str(resource(tm_subarraynode1).get("obsState"))
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
        resource(tm_subarraynode1).get("obsState"),
        resource(csp_subarray1).get("obsState"),
    ] == ["IDLE", "IDLE", "IDLE",]


def subarray_obs_state_is_empty():
   LOGGER.info(
        'resource(tm_subarraynode1).get("obsState")'
         + str(resource(tm_subarraynode1).get("obsState"))
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
        resource(tm_subarraynode1).get("obsState"),
        resource(csp_subarray1).get("obsState"),
    ] == ["EMPTY", "EMPTY", "EMPTY",]
