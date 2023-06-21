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
from typing import Optional


def check_state(state = None):
    # 
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
            resource(sdp_subarray1).get("State") in ["DISABLE", state],
            resource(sdp_master).get("State") in ["DISABLE", "STANDBY"],
            resource(csp_master).get("State") in ["DISABLE", "STANDBY"],
            resource(csp_subarray1).get("State") in ["DISABLE", state],
            resource(dish_master1).get("State") in ["DISABLE", "STANDBY"],
        ]
    )

def check_obs_state(obs_state = None):
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

    return all ([
        resource(sdp_subarray1).get("obsState") == obs_state,
        resource(tmc_subarraynode1).get("obsState") == obs_state,
        resource(csp_subarray1).get("obsState") == obs_state
    ] )


def tear_down(
    central_node, input_json: Optional[str] = None, raise_exception: Optional[bool] = True
):
    """Tears down the system after test run to get telescope back in standby
    state."""
    subarray_node_obsstate = resource(tmc_subarraynode1).get("obsState")

    if subarray_node_obsstate == "IDLE":
        LOGGER.info("Invoking ReleaseResources on TMC")
        central_node.invoke_release_resources(input_json)

        LOGGER.info("Invoking Telescope Standby on TMC")
        central_node.move_off()