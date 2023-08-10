"""Test cases for recovery of subarray stuck in RESOURCING
ObsState for mid"""
import json

import pytest
from ska_control_model import ObsState
from ska_tango_testing.mock.placeholders import Anything
from tango import DeviceProxy, EventType

from tests.conftest import LOGGER
from tests.resources.test_support.common_utils.common_helpers import (
    Resource,
    Waiter,
)
from tests.resources.test_support.common_utils.result_code import (
    FaultType,
    ResultCode,
)
from tests.resources.test_support.common_utils.telescope_controls import (
    BaseTelescopeControl,
)
from tests.resources.test_support.common_utils.tmc_helpers import (
    TmcHelper,
    tear_down,
)
from tests.resources.test_support.constant import (
    DEVICE_LIST_FOR_CHECK_DEVICES,
    DEVICE_OBS_STATE_EMPTY_INFO,
    DEVICE_STATE_ON_INFO,
    DEVICE_STATE_STANDBY_INFO,
    ON_OFF_DEVICE_COMMAND_DICT,
    centralnode,
    csp_subarray1,
    sdp_subarray1,
    tmc_sdp_subarray_leaf_node,
    tmc_subarraynode1,
)


@pytest.mark.SKA_mid
def test_recover_subarray_stuck_in_resourcing(
    json_factory, change_event_callbacks
):
    """AssignResources and ReleaseResources is executed."""
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")
    try:
        telescope_control = BaseTelescopeControl()
        tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)

        tmc_helper.check_devices(DEVICE_LIST_FOR_CHECK_DEVICES)

        # Verify Telescope is Off/Standby
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )
        LOGGER.info("Starting up the Telescope")

        # Invoke TelescopeOn() command on TMC
        tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)
        LOGGER.info("TelescopeOn command is invoked successfully")

        # Verify State transitions after TelescopeOn#
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_ON_INFO, "State"
        )

        the_waiter = Waiter()
        # Invoke AssignResources() Command on TMC
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")
        sdp_subarray = DeviceProxy(sdp_subarray1)
        central_node = DeviceProxy(centralnode)
        central_node.subscribe_event(
            "longRunningCommandResult",
            EventType.CHANGE_EVENT,
            change_event_callbacks["longRunningCommandResult"],
        )

        defect = {
            "enabled": True,
            "fault_type": FaultType.STUCK_IN_INTERMEDIATE_STATE,
            "error_message": "Device stuck in intermediate state",
            "result": ResultCode.FAILED,
            "intermediate_state": ObsState.RESOURCING,
        }
        sdp_subarray.SetDefective(json.dumps(defect))

        # Added this check to ensure that devices are running to avoid
        # random test failures.
        tmc_helper.check_devices(DEVICE_LIST_FOR_CHECK_DEVICES)
        Resource(tmc_subarraynode1).assert_attribute("State").equals("ON")
        Resource(tmc_subarraynode1).assert_attribute("obsState").equals(
            "EMPTY"
        )
        the_waiter.set_wait_for_specific_obsstate(
            "RESOURCING", [tmc_subarraynode1]
        )
        the_waiter.set_wait_for_specific_obsstate("IDLE", [csp_subarray1])
        _, unique_id = central_node.AssignResources(assign_json)
        the_waiter.wait(30)

        sdp_subarray.SetDefective(json.dumps({"enabled": False}))

        assertion_data = change_event_callbacks[
            "longRunningCommandResult"
        ].assert_change_event(
            (unique_id[0], Anything),
            lookahead=7,
        )
        assert "AssignResources" in assertion_data["attribute_value"][0]
        assert (
            "Timeout has occured, command failed"
            in assertion_data["attribute_value"][1]
        )
        assert (
            tmc_sdp_subarray_leaf_node in assertion_data["attribute_value"][1]
        )
        # as helper don't transition back themselves
        assert Resource(csp_subarray1).get("obsState") == "IDLE"
        assert Resource(sdp_subarray1).get("obsState") == "RESOURCING"
        sdp_subarray.SetDirectObsState(0)
        assert Resource(sdp_subarray1).get("obsState") == "EMPTY"
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

    except Exception as e:
        LOGGER.info(f"Exception occurred {e}")
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)
