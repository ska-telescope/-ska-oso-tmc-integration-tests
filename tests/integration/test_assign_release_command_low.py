from copy import deepcopy

import pytest
from tango import DeviceProxy, EventType

import tests.resources.test_support.low.tmc_helpers as tmc
from tests.conftest import LOGGER
from tests.resources.test_support.common_utils.common_helpers import Waiter
from tests.resources.test_support.common_utils.result_code import ResultCode
from tests.resources.test_support.common_utils.tmc_helpers import TmcHelper
from tests.resources.test_support.constant_low import (
    DEVICE_HEALTH_STATE_OK_INFO,
    DEVICE_OBS_STATE_ABORT_INFO,
    DEVICE_OBS_STATE_EMPTY_INFO,
    DEVICE_OBS_STATE_IDLE_INFO,
    DEVICE_STATE_OFF_INFO,
    DEVICE_STATE_ON_INFO,
    DEVICE_STATE_STANDBY_INFO,
    ON_OFF_DEVICE_COMMAND_DICT,
    centralnode,
    csp_subarray1,
    sdp_subarray1,
    tmc_csp_subarray_leaf_node,
    tmc_sdp_subarray_leaf_node,
    tmc_subarraynode1,
)
from tests.resources.test_support.low.helpers import resource
from tests.resources.test_support.low.sync_decorators import (
    sync_assign_resources,
)
from tests.resources.test_support.low.telescope_controls_low import (
    TelescopeControlLow,
)


# TODO:Create generic one tear down which can be utilized for both low and mid.
def tear_down_for_resourcing(tmc_helper, telescope_control):

    LOGGER.info("Invoking Abort on TMC")

    tmc_helper.invoke_abort(**ON_OFF_DEVICE_COMMAND_DICT)
    LOGGER.info("Invoking Abort command on TMC SubarrayNode")
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_ABORT_INFO, "obsState"
    )

    tmc_helper.invoke_restart(**ON_OFF_DEVICE_COMMAND_DICT)
    LOGGER.info("Invoking Restart command on TMC SubarrayNode")
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
    )

    tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)
    LOGGER.info("Invoking Standby command on TMC SubarrayNode")
    assert telescope_control.is_in_valid_state(
        DEVICE_STATE_STANDBY_INFO, "State"
    )

    LOGGER.info("Tear Down complete. Telescope is in Standby State")


@pytest.mark.SKA_low
def test_assign_release_low(json_factory):
    """AssignResources and ReleaseResources is executed."""
    try:
        telescope_control = TelescopeControlLow()
        assign_json = json_factory("command_assign_resource_low")
        release_json = json_factory("command_release_resource_low")
        tmc.check_devices()
        fixture = {}
        fixture["state"] = "Unknown"

        # Verify Telescope is Off/Standby
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )
        LOGGER.info("Staring up the Telescope")

        # Invoke TelescopeOn() command on TMC
        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
        tmc.set_to_on()
        LOGGER.info("TelescopeOn command is invoked successfully")

        # Verify State transitions after TelescopeOn
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_ON_INFO, "State"
        )
        fixture["state"] = "TelescopeOn"
        # The sleep solution is the temporary solution. Further investigation
        # needed

        # Invoke AssignResources() Command on TMC
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")

        @sync_assign_resources()
        def compose_sub():
            resource(tmc_subarraynode1).assert_attribute("State").equals("ON")
            resource(tmc_subarraynode1).assert_attribute("obsState").equals(
                "EMPTY"
            )
            central_node = DeviceProxy(centralnode)
            tmc.check_devices()
            tmc.check_telescope_availability()
            central_node.AssignResources(assign_json)
            LOGGER.info("Invoked AssignResources on CentralNode")

        compose_sub()

        LOGGER.info("AssignResources command is invoked successfully")

        # Verify ObsState is Idle
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_IDLE_INFO, "obsState"
        )
        fixture["state"] = "AssignResources"

        # Invoke ReleaseResources() command on TMC
        tmc.check_telescope_availability()
        tmc.invoke_releaseResources(release_json)

        fixture["state"] = "ReleaseResources"
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
        )

        tmc.check_telescope_availability()
        # Invoke TelescopeOff() command on TMC
        tmc.set_to_off()

        # Verify State transitions after TelescopeOff
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_OFF_INFO, "State"
        )
        fixture["state"] = "TelescopeOff"

        LOGGER.info("Tests complete.")

    except Exception:
        if fixture["state"] == "AssignResources":
            tmc.invoke_releaseResources(release_json)
        if fixture["state"] == "TelescopeOn":
            tmc.set_to_off()
        raise


@pytest.mark.skip(
    reason="Abort command is not implemented on SDP Subarray Leaf Node."
)
@pytest.mark.SKA_low
def test_assign_release_timeout(json_factory, change_event_callbacks):
    """Verify timeout exception raised when csp set to defective."""
    assign_json = json_factory("command_assign_resource_low")
    release_json = json_factory("command_release_resource_low")
    try:
        telescope_control = TelescopeControlLow()
        tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)

        fixture = {}
        fixture["state"] = "Unknown"

        # Verify Telescope is Off/Standby
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )

        # Invoke TelescopeOn() command on TMC
        tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify State transitions after TelescopeOn
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_ON_INFO, "State"
        )
        fixture["state"] = "TelescopeOn"

        # Invoke AssignResources() Command on TMC
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")
        # Verify State transitions after TelescopeOn

        central_node = DeviceProxy(centralnode)
        central_node.subscribe_event(
            "longRunningCommandResult",
            EventType.CHANGE_EVENT,
            change_event_callbacks["longRunningCommandResult"],
        )

        csp_subarray = DeviceProxy(csp_subarray1)
        csp_subarray.SetDefective(True)

        device_params = deepcopy(ON_OFF_DEVICE_COMMAND_DICT)
        device_params["set_wait_for_obsstate"] = False
        result, unique_id = tmc_helper.compose_sub(
            assign_json, **device_params
        )

        LOGGER.info(f"Command result {result} and unique id {unique_id}")

        assert unique_id[0].endswith("AssignResources")
        assert result[0] == ResultCode.QUEUED

        exception_message = (
            f"Exception occured on device: "
            f"{tmc_subarraynode1}: Exception occured on device"
            f": {tmc_csp_subarray_leaf_node}: Timeout has "
            f"occured, command failed"
        )

        change_event_callbacks["longRunningCommandResult"].assert_change_event(
            (unique_id[0], exception_message),
            lookahead=7,
        )
        csp_subarray.SetDefective(False)

        tear_down_for_resourcing(tmc_helper, telescope_control)

    except Exception:
        if fixture["state"] == "AssignResources":
            tmc.invoke_releaseResources(release_json)
        if fixture["state"] == "TelescopeOn":
            tmc.set_to_off()
        raise


@pytest.mark.skip(
    reason="Abort command is not implemented on SDP Subarray Leaf Node."
)
@pytest.mark.SKA_low
def test_assign_release_timeout_sdp(json_factory, change_event_callbacks):
    """Verify timeout exception raised when sdp set to defective."""
    assign_json = json_factory("command_assign_resource_low")
    release_json = json_factory("command_release_resource_low")
    try:
        telescope_control = TelescopeControlLow()
        tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)

        fixture = {}
        fixture["state"] = "Unknown"

        # Verify Telescope is Off/Standby
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )

        # Invoke TelescopeOn() command on TMC
        tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify State transitions after TelescopeOn
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_ON_INFO, "State"
        )
        fixture["state"] = "TelescopeOn"

        # Invoke AssignResources() Command on TMC
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")
        # Verify State transitions after TelescopeOn

        central_node = DeviceProxy(centralnode)
        central_node.subscribe_event(
            "longRunningCommandResult",
            EventType.CHANGE_EVENT,
            change_event_callbacks["longRunningCommandResult"],
        )

        sdp_subarray = DeviceProxy(sdp_subarray1)
        sdp_subarray.SetDefective(True)

        device_params = deepcopy(ON_OFF_DEVICE_COMMAND_DICT)
        device_params["set_wait_for_obsstate"] = False
        result, unique_id = tmc_helper.compose_sub(
            assign_json, **device_params
        )

        LOGGER.info(f"Command result {result} and unique id {unique_id}")

        assert unique_id[0].endswith("AssignResources")
        assert result[0] == ResultCode.QUEUED

        exception_message = (
            f"Exception occured on device: "
            f"{tmc_subarraynode1}: Exception occured on device"
            f": {tmc_sdp_subarray_leaf_node}: Timeout has "
            f"occured, command failed"
        )

        change_event_callbacks["longRunningCommandResult"].assert_change_event(
            (unique_id[0], exception_message),
            lookahead=7,
        )
        sdp_subarray.SetDefective(False)

        tear_down_for_resourcing(tmc_helper, telescope_control)

    except Exception:
        if fixture["state"] == "AssignResources":
            tmc.invoke_releaseResources(release_json)
        if fixture["state"] == "TelescopeOn":
            tmc.set_to_off()
        raise


@pytest.mark.skip(
    reason="will be enabled when new tag of \
        SDP Subarray Leaf Node will release"
)
@pytest.mark.SKA_low
def test_health_check_low():
    telescope_control = TelescopeControlLow()
    assert telescope_control.is_in_valid_state(
        DEVICE_HEALTH_STATE_OK_INFO, "healthState"
    )


@pytest.mark.SKA_low
def test_release_exception_propagation(json_factory, change_event_callbacks):
    """Verify timeout exception raised when csp set to defective."""
    assign_json = json_factory("command_assign_resource_low")
    release_json = json_factory("command_release_resource_low")
    telescope_control = TelescopeControlLow()
    tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)
    try:
        # Verify Telescope is Off/Standby
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )

        # Invoke TelescopeOn() command on TMC
        tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify State transitions after TelescopeOn
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_ON_INFO, "State"
        )

        tmc_helper.compose_sub(assign_json, **ON_OFF_DEVICE_COMMAND_DICT)

        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_IDLE_INFO, "obsState"
        )

        central_node = DeviceProxy(centralnode)
        central_node.subscribe_event(
            "longRunningCommandResult",
            EventType.CHANGE_EVENT,
            change_event_callbacks["longRunningCommandResult"],
        )

        csp_subarray = DeviceProxy(csp_subarray1)
        csp_subarray.SetDefective(True)

        device_params = deepcopy(ON_OFF_DEVICE_COMMAND_DICT)
        device_params["set_wait_for_obsstate"] = False
        result, unique_id = tmc_helper.invoke_releaseResources(
            release_json, **device_params
        )

        assert unique_id[0].endswith("ReleaseResources")
        assert result[0] == ResultCode.QUEUED

        exception_message = (
            f"Exception occured on device: "
            f"{tmc_subarraynode1}: Exception occured on device"
            f": {tmc_csp_subarray_leaf_node}: Timeout has "
            f"occured, command failed"
        )

        change_event_callbacks["longRunningCommandResult"].assert_change_event(
            (unique_id[0], exception_message),
            lookahead=7,
        )
        change_event_callbacks["longRunningCommandResult"].assert_change_event(
            (unique_id[0], str(ResultCode.FAILED.value)),
            lookahead=7,
        )

        csp_subarray.SetDefective(False)

        # Simulating Csp Subarray going back to IDLE after command failure
        csp_subarray.SetDirectObsState(2)

        # Tear Down
        csp_sln = DeviceProxy(tmc_csp_subarray_leaf_node)
        csp_sln.ReleaseAllResources()

        waiter = Waiter(**ON_OFF_DEVICE_COMMAND_DICT)
        waiter.set_wait_for_going_to_empty()
        waiter.wait(200)
        subarray_node = DeviceProxy(tmc_subarraynode1)
        resource(subarray_node).assert_attribute("obsState").equals("EMPTY")

        tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )

        LOGGER.info("Tear Down complete. Telescope is in Standby State")

    except Exception as e:
        LOGGER.info("Exception occured during test run: %s", e)
        tear_down_for_resourcing(tmc_helper, telescope_control)
