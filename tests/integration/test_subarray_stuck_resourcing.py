import pytest
from ska_tango_base.control_model import ObsState
from tango import DeviceProxy, EventType

from tests.conftest import LOGGER
from tests.resources.test_support.common_utils.tmc_helpers import TmcHelper
from tests.resources.test_support.constant import (
    DEVICE_LIST_FOR_CHECK_DEVICES,
    DEVICE_OBS_STATE_EMPTY_INFO,
    DEVICE_STATE_ON_INFO,
    DEVICE_STATE_STANDBY_INFO,
    ON_OFF_DEVICE_COMMAND_DICT,
    centralnode,
    csp_subarray1,
    sdp_subarray1,
    tmc_subarraynode1,
)
from tests.resources.test_support.helpers import resource, waiter
from tests.resources.test_support.telescope_controls import (
    BaseTelescopeControl,
)


@pytest.mark.SKA_mid
def test_assign_release(json_factory, change_event_callbacks):
    """AssignResources and ReleaseResources is executed."""
    assign_json = json_factory("command_AssignResources")

    telescope_control = BaseTelescopeControl()
    tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)

    tmc_helper.check_devices(DEVICE_LIST_FOR_CHECK_DEVICES)

    # Verify Telescope is Off/Standby
    assert telescope_control.is_in_valid_state(
        DEVICE_STATE_STANDBY_INFO, "State"
    )
    LOGGER.info("Staring up the Telescope")

    # Invoke TelescopeOn() command on TMC
    LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
    tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)
    LOGGER.info("TelescopeOn command is invoked successfully")

    # Verify State transitions after TelescopeOn
    # Verify State transitions after TelescopeOn#
    assert telescope_control.is_in_valid_state(DEVICE_STATE_ON_INFO, "State")

    the_waiter = waiter()
    # Invoke AssignResources() Command on TMC
    LOGGER.info("Invoking AssignResources command on TMC CentralNode")
    sdp_subarray = DeviceProxy(sdp_subarray1)
    central_node = DeviceProxy(centralnode)
    central_node.subscribe_event(
        "longRunningCommandResult",
        EventType.CHANGE_EVENT,
        change_event_callbacks["longRunningCommandResult"],
    )

    sdp_subarray.SetRaiseException(True)

    # Added this check to ensure that devices are running to avoid
    # random test failures.
    global unique_id, result_code
    tmc_helper.check_devices(DEVICE_LIST_FOR_CHECK_DEVICES)
    resource(tmc_subarraynode1).assert_attribute("State").equals("ON")
    resource(tmc_subarraynode1).assert_attribute("obsState").equals("EMPTY")
    the_waiter.set_wait_for_specific_obsstate(
        "RESOURCING", [sdp_subarray1, tmc_subarraynode1]
    )
    the_waiter.set_wait_for_specific_obsstate("IDLE", [csp_subarray1])
    result_code, unique_id = central_node.AssignResources(assign_json)
    the_waiter.wait(30)

    sdp_subarray.SetRaiseException(False)

    change_event_callbacks["longRunningCommandResult"].assert_change_event(
        (
            unique_id[0],
            "Exception occured on device: ska_mid/tm_subarray_node/1: "
            + "Timeout has occured, command failed",
        ),
        lookahead=7,
    )
    sdp_subarray.SetDirectObsState(
        ObsState.EMPTY
    )  # as helper don't transition back themselves
    assert resource(csp_subarray1).get("obsState") == "IDLE"

    assert resource(sdp_subarray1).get("obsState") == "EMPTY"
    csp_subarray = DeviceProxy(csp_subarray1)
    csp_subarray.ReleaseAllResources()
    the_waiter.set_wait_for_specific_obsstate("EMPTY", [csp_subarray1])
    the_waiter.set_wait_for_specific_obsstate("EMPTY", [tmc_subarraynode1])
    the_waiter.wait(30)

    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
    )

    # Invoke TelescopeStandby() command on TMC#
    tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)

    # Verify State transitions after TelescopeStandby#
    assert telescope_control.is_in_valid_state(
        DEVICE_STATE_STANDBY_INFO, "State"
    )

    LOGGER.info("Test complete.")
