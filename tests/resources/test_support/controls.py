# local depencies
from tests.conftest import LOGGER
from tests.resources.test_support.constant import (
    centralnode,
    csp_master,
    csp_subarray1,
    dish_master1,
    sdp_master,
    sdp_subarray1,
    tmc_subarraynode1,
)
from tests.resources.test_support.helpers import resource


def telescope_is_in_standby_state():
    LOGGER.info(
        f"{sdp_master}.State : " + str(resource(sdp_master).get("State"))
    )
    LOGGER.info(
        f"{sdp_subarray1}.State : " + str(resource(sdp_subarray1).get("State"))
    )
    LOGGER.info(
        f"{csp_master}.State : " + str(resource(csp_master).get("State"))
    )
    LOGGER.info(
        f"{csp_subarray1}.State : " + str(resource(csp_subarray1).get("State"))
    )
    LOGGER.info(
        f"{dish_master1}.State : " + str(resource(dish_master1).get("State"))
    )

    return all(
        [
            resource(sdp_subarray1).get("State") in ["DISABLE", "OFF"],
            resource(sdp_master).get("State") in ["DISABLE", "STANDBY"],
            resource(csp_master).get("State") in ["DISABLE", "STANDBY"],
            resource(csp_subarray1).get("State") in ["DISABLE", "OFF"],
            resource(dish_master1).get("State") in ["DISABLE", "STANDBY"],
        ]
    )


def telescope_is_in_on_state():
    LOGGER.info(
        f"{tmc_subarraynode1}.State : "
        + str(resource(tmc_subarraynode1).get("State"))
    )
    LOGGER.info(
        f"{sdp_master}.State : " + str(resource(sdp_master).get("State"))
    )
    LOGGER.info(
        f"{sdp_subarray1}.State : " + str(resource(sdp_subarray1).get("State"))
    )
    LOGGER.info(
        f"{csp_master}.State : " + str(resource(csp_master).get("State"))
    )
    LOGGER.info(
        f"{csp_subarray1}.State : " + str(resource(csp_subarray1).get("State"))
    )
    LOGGER.info(
        f"{dish_master1}.State : " + str(resource(dish_master1).get("State"))
    )
    LOGGER.info(
        f"{centralnode}.State : " + str(resource(centralnode).get("State"))
    )

    return [
        resource(sdp_subarray1).get("State"),
        resource(sdp_master).get("State"),
        resource(csp_master).get("State"),
        resource(csp_subarray1).get("State"),
        resource(dish_master1).get("State"),
        resource(centralnode).get("State"),
    ] == ["ON", "ON", "ON", "ON", "STANDBY", "ON"]


def telescope_is_in_off_state():
    LOGGER.info(
        f"{sdp_master}.State : " + str(resource(sdp_master).get("State"))
    )
    LOGGER.info(
        f"{sdp_subarray1}.State : " + str(resource(sdp_subarray1).get("State"))
    )
    LOGGER.info(
        f"{csp_master}.State : " + str(resource(csp_master).get("State"))
    )
    LOGGER.info(
        f"{csp_subarray1}.State : " + str(resource(csp_subarray1).get("State"))
    )
    LOGGER.info(
        f"{dish_master1}.State : " + str(resource(dish_master1).get("State"))
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
        f"{tmc_subarraynode1}.obsState : "
        + str(resource(tmc_subarraynode1).get("obsState"))
    )
    LOGGER.info(
        f"{sdp_subarray1}.obsState : "
        + str(resource(sdp_subarray1).get("obsState"))
    )
    LOGGER.info(
        f"{csp_subarray1}.obsState : "
        + str(resource(csp_subarray1).get("obsState"))
    )

    return [
        resource(sdp_subarray1).get("obsState"),
        resource(tmc_subarraynode1).get("obsState"),
        resource(csp_subarray1).get("obsState"),
    ] == [
        "IDLE",
        "IDLE",
        "IDLE",
    ]


def subarray_obs_state_is_empty():
    LOGGER.info(
        f"{tmc_subarraynode1}.obsState : "
        + str(resource(tmc_subarraynode1).get("obsState"))
    )
    LOGGER.info(
        f"{sdp_subarray1}.obsState : "
        + str(resource(sdp_subarray1).get("obsState"))
    )
    LOGGER.info(
        f"{csp_subarray1}.obsState : "
        + str(resource(csp_subarray1).get("obsState"))
    )

    return [
        resource(sdp_subarray1).get("obsState"),
        resource(tmc_subarraynode1).get("obsState"),
        resource(csp_subarray1).get("obsState"),
    ] == [
        "EMPTY",
        "EMPTY",
        "EMPTY",
    ]


def subarray_obs_state_is_ready():
    LOGGER.info(
        f"{tmc_subarraynode1}.obsState : "
        + str(resource(tmc_subarraynode1).get("obsState"))
    )
    LOGGER.info(
        f"{sdp_subarray1}.obsState : "
        + str(resource(sdp_subarray1).get("obsState"))
    )
    LOGGER.info(
        f"{csp_subarray1}.obsState : "
        + str(resource(csp_subarray1).get("obsState"))
    )

    return [
        resource(sdp_subarray1).get("obsState"),
        resource(tmc_subarraynode1).get("obsState"),
        resource(csp_subarray1).get("obsState"),
    ] == [
        "READY",
        "READY",
        "READY",
    ]


def subarray_obs_state_is_aborted():
    LOGGER.info(
        f"{tmc_subarraynode1}.obsState : "
        + str(resource(tmc_subarraynode1).get("obsState"))
    )
    LOGGER.info(
        f"{sdp_subarray1}.obsState : "
        + str(resource(sdp_subarray1).get("obsState"))
    )
    LOGGER.info(
        f"{csp_subarray1}.obsState : "
        + str(resource(csp_subarray1).get("obsState"))
    )

    return [
        resource(sdp_subarray1).get("obsState"),
        resource(tmc_subarraynode1).get("obsState"),
        resource(csp_subarray1).get("obsState"),
    ] == [
        "ABORTED",
        "ABORTED",
        "ABORTED",
    ]
