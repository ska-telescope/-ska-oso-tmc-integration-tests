##local depencies
from tests.resources.test_support.helpers import (
    resource
)
from tests.conftest import LOGGER    

def telescope_is_in_standby_state():
    LOGGER.info(
        'resource("ska_mid/tm_subarray_node/1").get("State")'
        + str(resource("ska_mid/tm_subarray_node/1").get("State"))
    )
    LOGGER.info(
        'resource("mid_sdp/elt/master").get("State")'
        + str(resource("mid_sdp/elt/master").get("State"))
    )
    LOGGER.info(
        'resource("mid_sdp/elt/subarray_1").get("State")'
        + str(resource("mid_sdp/elt/subarray_1").get("State"))
    )
    LOGGER.info(
        'resource("mid_csp/elt/master").get("State")'
        + str(resource("mid_csp/elt/master").get("State"))
    )
    LOGGER.info(
        'resource("mid_csp/elt/subarray_01").get("State")'
        + str(resource("mid_csp/elt/subarray_01").get("State"))
    )
    LOGGER.info(
        'resource("mid_d0001/elt/master").get("State")'
        + str(resource("mid_d0001/elt/master").get("State"))
    )
    LOGGER.info(
        'resource("ska_mid/tm_central/central_node").get("State")'
        + str(resource("ska_mid/tm_central/central_node").get("State"))
    )
    LOGGER.info(
        'resource("ska_mid/tm_central/central_node").get("telescopeState")'
        + str(resource("ska_mid/tm_central/central_node").get("telescopeState")))

    return (resource("mid_sdp/elt/subarray_1").get("State") in ["DISABLE" , "OFF"],
    resource("mid_sdp/elt/master").get("State") in ["DISABLE", "STANDBY"],
    resource("mid_csp/elt/master").get("State") in ["DISABLE", "STANDBY"],
    resource("mid_csp/elt/subarray_01").get("State") in ["DISABLE", "OFF"],
    resource("mid_d0001/elt/master").get("State") in ["DISABLE", "OFF"],
)

def telescope_is_in_on_state():
    LOGGER.info(
        'resource("ska_mid/tm_subarray_node/1").get("State")'
        + str(resource("ska_mid/tm_subarray_node/1").get("State"))
    )
    LOGGER.info(
        'resource("mid_sdp/elt/master").get("State")'
        + str(resource("mid_sdp/elt/master").get("State"))
    )
    LOGGER.info(
        'resource("mid_sdp/elt/subarray_1").get("State")'
        + str(resource("mid_sdp/elt/subarray_1").get("State"))
    )
    LOGGER.info(
        'resource("ska_mid/tm_central/central_node").get("State")'
        + str(resource("ska_mid/tm_central/central_node").get("State")))

    LOGGER.info(
        'resource("mid_csp/elt/master").get("State")'
        + str(resource("mid_csp/elt/master").get("State"))
    )
    LOGGER.info(
        'resource("mid_csp/elt/subarray_01").get("State")'
        + str(resource("mid_csp/elt/subarray_01").get("State"))
    )
    LOGGER.info(
        'resource("mid_d0001/elt/master").get("State")'
        + str(resource("mid_d0001/elt/master").get("State"))
    )
    LOGGER.info(
        'resource("ska_mid/tm_central/central_node").get("telescopeState")'
        + str(resource("ska_mid/tm_central/central_node").get("telescopeState")))

    return [
        resource("mid_sdp/elt/subarray_1").get("State"),
        resource("mid_sdp/elt/master").get("State"),
        resource("mid_csp/elt/master").get("State"),
        resource("mid_csp/elt/subarray_01").get("State"),
        resource("mid_d0001/elt/master").get("State"),
        resource("ska_mid/tm_central/central_node").get("State"),
        resource("ska_mid/tm_central/central_node").get("telescopeState"),
    ] == ["ON", "ON", "ON", "ON", "ON", "ON", "ON"]


def telescope_is_in_off_state():
    LOGGER.info(
        'resource("ska_mid/tm_subarray_node/1").get("State")'
        + str(resource("ska_mid/tm_subarray_node/1").get("State"))
    )
    LOGGER.info(
        'resource("mid_sdp/elt/master").get("State")'
        + str(resource("mid_sdp/elt/master").get("State"))
    )
    LOGGER.info(
        'resource("mid_sdp/elt/subarray_1").get("State")'
        + str(resource("mid_sdp/elt/subarray_1").get("State"))
    )
    LOGGER.info(
        'resource("ska_mid/tm_central/central_node").get("State")'
        + str(resource("ska_mid/tm_central/central_node").get("State")))

    LOGGER.info(
        'resource("mid_csp/elt/master").get("State")'
        + str(resource("mid_csp/elt/master").get("State"))
    )
    LOGGER.info(
        'resource("mid_csp/elt/subarray_01").get("State")'
        + str(resource("mid_csp/elt/subarray_01").get("State"))
    )
    LOGGER.info(
        'resource("mid_d0001/elt/master").get("State")'
        + str(resource("mid_d0001/elt/master").get("State"))
    )

    LOGGER.info(
        'resource("ska_mid/tm_central/central_node").get("telescopeState")'
        + str(resource("ska_mid/tm_central/central_node").get("telescopeState")))

    return [
        resource("mid_sdp/elt/subarray_1").get("State"),
        resource("mid_sdp/elt/master").get("State"),
        resource("mid_csp/elt/master").get("State"),
        resource("mid_csp/elt/subarray_01").get("State"),
        resource("mid_d0001/elt/master").get("State"),
        resource("ska_mid/tm_central/central_node").get("State"),
        resource("ska_mid/tm_central/central_node").get("telescopeState"),
    ] == ["OFF", "OFF", "STANDBY", "OFF", "OFF", "ON", "STANDBY"]


def subarray_obs_state_is_idle ():
   LOGGER.info(
        'resource("ska_mid/tm_subarray_node/1").get("obsState")'
         + str(resource("ska_mid/tm_subarray_node/1").get("obsState"))
    )
   LOGGER.info(
        'resource("mid_sdp/elt/subarray_1").get("obsState")'
         + str(resource("mid_sdp/elt/subarray_1").get("obsState"))
    )
   LOGGER.info(
        'resource("mid_csp/elt/subarray_01").get("obsState")'
         + str(resource("mid_csp/elt/subarray_01").get("obsState"))
    )
   
   return [
        resource("mid_sdp/elt/subarray_1").get("obsState"),
        resource("ska_mid/tm_subarray_node/1").get("obsState"),
        resource("mid_csp/elt/subarray_01").get("obsState"),
    ] == ["IDLE", "IDLE", "IDLE",]


def subarray_obs_state_is_empty():
   LOGGER.info(
        'resource("ska_mid/tm_subarray_node/1").get("obsState")'
         + str(resource("ska_mid/tm_subarray_node/1").get("obsState"))
    )
   LOGGER.info(
        'resource("mid_sdp/elt/subarray_1").get("obsState")'
         + str(resource("mid_sdp/elt/subarray_1").get("obsState"))
    )
   LOGGER.info(
        'resource("mid_csp/elt/subarray_01").get("obsState")'
         + str(resource("mid_csp/elt/subarray_01").get("obsState"))
    )
   
   return [
        resource("mid_sdp/elt/subarray_1").get("obsState"),
        resource("ska_mid/tm_subarray_node/1").get("obsState"),
        resource("mid_csp/elt/subarray_01").get("obsState"),
    ] == ["EMPTY", "EMPTY", "EMPTY",]
