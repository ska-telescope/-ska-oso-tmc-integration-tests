from typing import Optional

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


def check_subarray_state(state=None):
    LOGGER.info(
        f"{tmc_subarraynode1}.State : "
        + str(resource(tmc_subarraynode1).get("State"))
    )

    return resource(tmc_subarraynode1).get("State") in ["DISABLE", state]


def check_obs_state(obs_state=None):
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

    return all(
        [
            resource(sdp_subarray1).get("obsState") == obs_state,
            resource(tmc_subarraynode1).get("obsState") == obs_state,
            resource(csp_subarray1).get("obsState") == obs_state,
        ]
    )


def tear_down(
    central_node,
    input_json: Optional[str] = None,
    raise_exception: Optional[bool] = True,
):
    """Tears down the system after test run to get telescope back in standby
    state."""
    subarray_node_obsstate = resource(tmc_subarraynode1).get("obsState")

    if subarray_node_obsstate == "IDLE":
        LOGGER.info("Invoking ReleaseResources on TMC")
        central_node.invoke_release_resources(input_json)

        LOGGER.info("Invoking Telescope Standby on TMC")
        central_node.move_off()
