from typing import Optional

from tests.conftest import LOGGER
from tests.resources.test_support.common_utils.common_helpers import (
    Waiter,
    resource,
)
from tests.resources.test_support.constant import (
    csp_subarray1,
    dish_master1,
    sdp_subarray1,
    tmc_subarraynode1,
)


def check_subarray_obs_state(obs_state=None, timeout=500):

    device_dict = {
        "sdp_subarray": sdp_subarray1,
        "csp_subarray": csp_subarray1,
        "tmc_subarraynode": tmc_subarraynode1,
    }

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
    if obs_state == "READY":
        device_dict["dish_master"] = dish_master1
    the_waiter = Waiter(**device_dict)
    the_waiter.set_wait_for_obs_state(obs_state=obs_state)
    the_waiter.wait(timeout)

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
