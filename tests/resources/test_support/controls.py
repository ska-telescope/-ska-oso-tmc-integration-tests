# local depencies
from tests.resources.test_support.helpers import (
    resource
)
from tests.conftest import LOGGER

centralnode = "ska_mid/tm_central/central_node"
tm_subarraynode1 = "ska_mid/tm_subarray_node/1"
tm_subarraynode2 = "ska_mid/tm_subarray_node/2"
tm_subarraynode3 = "ska_mid/tm_subarray_node/3"
sdp_subarray1 = "mid-sdp/subarray/01"
sdp_subarray2 = "mid-sdp/subarray/02"
sdp_subarray3 = "mid-sdp/subarray/03"
csp_subarray1 = "mid-csp/subarray/01"
csp_subarray2 = "mid-csp/subarray/02"
csp_subarray3 = "mid-csp/subarray/03"
sdp_master = "mid_sdp/elt/master"
csp_master = "mid-csp/control/0"
dish_master1 = "mid_d0001/elt/master"
dish_master2 = "mid_d0002/elt/master"
dish_master3 = "mid_d0003/elt/master"
dish_master4 = "mid_d0004/elt/master"


def telescope_is_in_standby_state():
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
    ] == ["OFF", "OFF", "OFF", "OFF", "STANDBY", "ON"]


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
