import pytest
from datetime import date, datetime
import os
import logging
from tango import DevState

##local depencies
from tests.resources.test_support.helpers import (
    resource
)

LOGGER = logging.getLogger(__name__)


def telescope_is_in_standby():
    LOGGER.info(
        'resource("ska_mid/tm_subarray_node/1").get("State")'
        + str(resource("ska_mid/tm_subarray_node/1").get("State"))
    )
    LOGGER.info(
        'resource("mid_sdp/elt/subarray_1").get("State")'
        + str(resource("mid_sdp/elt/subarray_1").get("State"))
    )
    LOGGER.info(
        'resource("mid_sdp/elt/master").get("State")'
        + str(resource("mid_sdp/elt/master").get("State"))
    )

    # TODO: Check for sdp Subarray state to be added
    # return [
    #     resource("ska_mid/tm_subarray_node/1").get("State"),
    #     resource("mid_csp/elt/subarray_01").get("State"),
    #     resource("mid_csp_cbf/sub_elt/subarray_01").get("State"),
    # ] == ["OFF", "OFF", "OFF"]

    return [
        resource("mid_sdp/elt/subarray_1").get("State"),
        resource("mid_sdp/elt/master").get("State")
    ] == ["OFF", "OFF"]


def telescope_is_in_on():
    LOGGER.info(
        'resource("mid_sdp/elt/subarray_1").get("State")'
        + str(resource("mid_sdp/elt/subarray_1").get("State"))
    )
    LOGGER.info(
        'resource("mid_sdp/elt/master").get("State")'
        + str(resource("mid_sdp/elt/master").get("State"))
    )
    LOGGER.info(
        'resource("ska_mid/tm_central/central_node").get("State")'
        + str(resource("ska_mid/tm_central/central_node").get("State"))
    )
    LOGGER.info(
        'resource("mid_sdp/elt/subarray_1").get("State")'
        + str(resource("mid_sdp/elt/subarray_1").get("State"))
    )

    return [
        resource("mid_sdp/elt/subarray_1").get("State"),
        resource("mid_sdp/elt/master").get("State"),
        resource("ska_mid/tm_central/central_node").get("State"),
        resource("ska_mid/tm_central/central_node").get("telescopeState"),
    ] == ["ON", "ON", "ON", "UNKNOWN"]

def telescope_is_in_off():
    LOGGER.info(
        'resource("mid_sdp/elt/subarray_1").get("State")'
        + str(resource("mid_sdp/elt/subarray_1").get("State"))
    )
    LOGGER.info(
        'resource("mid_sdp/elt/master").get("State")'
        + str(resource("mid_sdp/elt/master").get("State"))
    )
    LOGGER.info(
        'resource("ska_mid/tm_central/central_node").get("State")'
        + str(resource("ska_mid/tm_central/central_node").get("State"))
    )
    LOGGER.info(
        'resource("mid_sdp/elt/subarray_1").get("State")'
        + str(resource("mid_sdp/elt/subarray_1").get("State"))
    )

    return [
        resource("mid_sdp/elt/subarray_1").get("State"),
        resource("mid_sdp/elt/master").get("State"),
        resource("ska_mid/tm_central/central_node").get("State"),
        resource("ska_mid/tm_central/central_node").get("telescopeState"),
    ] == ["OFF", "OFF", "ON", "UNKNOWN"]
