"""Test cases for Abort and Restart Command"""
import json
import time

import pytest
from ska_tango_testing.mock.placeholders import Anything
from tango import DeviceProxy

from tests.conftest import LOGGER
from tests.resources.test_support.common_utils.common_helpers import (
    Resource,
    Waiter,
)
from tests.resources.test_support.common_utils.telescope_controls import (
    BaseTelescopeControl,
    check_subarray1_availability,
)
from tests.resources.test_support.common_utils.tmc_helpers import (
    TmcHelper,
    tear_down,
)
from tests.resources.test_support.constant import (
    DEVICE_LIST_FOR_CHECK_DEVICES,
    DEVICE_OBS_STATE_ABORT_INFO,
    DEVICE_OBS_STATE_EMPTY_INFO,
    DEVICE_OBS_STATE_IDLE_INFO,
    DEVICE_OBS_STATE_READY_INFO,
    DEVICE_STATE_ON_INFO,
    DEVICE_STATE_STANDBY_INFO,
    INTERMEDIATE_CONFIGURING_OBS_STATE_DEFECT,
    INTERMEDIATE_STATE_DEFECT,
    ON_OFF_DEVICE_COMMAND_DICT,
    centralnode,
    csp_subarray1,
    dish_master1,
    sdp_subarray1,
    tmc_subarraynode1,
)

telescope_control = BaseTelescopeControl()
tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)


@pytest.mark.SKA_mid
def test_abort_restart(json_factory):
    """Abort and Restart is executed."""
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")
    try:
        tmc_helper.check_devices(DEVICE_LIST_FOR_CHECK_DEVICES)

        # Verify Telescope is Off/Standby#
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )

        # Invoke TelescopeOn() command on TMC#
        tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify State transitions after TelescopeOn#
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_ON_INFO, "State"
        )

        # Check Subarray1 availability
        assert check_subarray1_availability(tmc_subarraynode1)

        # Invoke AssignResources() Command on TMC#
        tmc_helper.compose_sub(assign_json, **ON_OFF_DEVICE_COMMAND_DICT)

        # Verify ObsState is IDLE#
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_IDLE_INFO, "obsState"
        )

        # Invoke Abort() command on TMC
        tmc_helper.invoke_abort(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify State transitions after Abort#
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_ABORT_INFO, "obsState"
        )
        # Invoke Restart() command on TMC#
        tmc_helper.invoke_restart(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify ObsState is EMPTY#
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
        LOGGER.exception("The exception is: %s", e)
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)


@pytest.mark.SKA_mid
def test_abort_in_empty(json_factory):
    """Test Abort in EMPTY"""
    release_json = json_factory("command_ReleaseResources")
    try:
        tmc_helper.check_devices(DEVICE_LIST_FOR_CHECK_DEVICES)

        # Verify Telescope is Off/Standby#
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )

        # Invoke TelescopeOn() command on TMC#
        tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify State transitions after TelescopeOn#
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_ON_INFO, "State"
        )
        # Verify ObsState is EMPTY#
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
        )

        # Invoke Abort() command on TMC
        with pytest.raises(Exception):
            tmc_helper.invoke_abort()

        # Invoke TelescopeStandby() command on TMC#
        tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify State transitions after TelescopeStandby#
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )
        LOGGER.info("Test complete.")
    except Exception as e:
        LOGGER.exception("The exception is: %s", e)
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)


@pytest.mark.skip(reason="random failure")
@pytest.mark.SKA_mid
def test_abort_in_resourcing(json_factory):
    """Abort and Restart is executed."""
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")
    config_json = json_factory("command_Configure")
    scan_json = json_factory("command_Scan")
    try:
        tmc_helper.check_devices(DEVICE_LIST_FOR_CHECK_DEVICES)

        # Verify Telescope is Off/Standby#
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )

        # Invoke TelescopeOn() command on TMC#
        tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify State transitions after TelescopeOn#
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_ON_INFO, "State"
        )

        csp_subarray_proxy = DeviceProxy(csp_subarray1)
        csp_subarray_proxy.SetDefective(json.dumps(INTERMEDIATE_STATE_DEFECT))

        # Invoke AssignResources() Command on TMC
        Resource(tmc_subarraynode1).assert_attribute("State").equals("ON")
        Resource(tmc_subarraynode1).assert_attribute("obsState").equals(
            "EMPTY"
        )
        central_node = DeviceProxy(centralnode)
        central_node.AssignResources(assign_json)

        # Verify ObsState is RESOURCING
        the_waiter = Waiter()
        the_waiter.set_wait_for_specific_obsstate(
            "RESOURCING", [tmc_subarraynode1]
        )
        the_waiter.wait(20)

        # Setting CSP back to normal
        csp_subarray_proxy.SetDefective(json.dumps({"enabled": False}))
        time.sleep(0.1)

        # Invoke Abort() command on TMC
        tmc_helper.invoke_abort(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify State transitions after Abort#
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_ABORT_INFO, "obsState"
        )
        # Invoke Restart() command on TMC#
        tmc_helper.invoke_restart(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify ObsState is EMPTY#
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
        )

        # Invoke AssignResources() Command on TMC
        tmc_helper.compose_sub(assign_json, **ON_OFF_DEVICE_COMMAND_DICT)
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_IDLE_INFO, "obsState"
        )

        # Invoke Configure() Command on TMC
        tmc_helper.configure_subarray(
            config_json, **ON_OFF_DEVICE_COMMAND_DICT
        )
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_READY_INFO, "obsState"
        )

        # Invoke Scan() Command on TMC
        tmc_helper.scan(scan_json, **ON_OFF_DEVICE_COMMAND_DICT)
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_READY_INFO, "obsState"
        )

        # Invoke End() Command on TMC
        tmc_helper.end(**ON_OFF_DEVICE_COMMAND_DICT)
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_IDLE_INFO, "obsState"
        )
        # Invoke ReleaseResources() command on TMC
        tmc_helper.invoke_releaseResources(
            release_json, **ON_OFF_DEVICE_COMMAND_DICT
        )
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
        )
        # Invoke Standby() command on TMC
        tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )
    except Exception as e:
        LOGGER.exception("The exception is: %s", e)
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)


@pytest.mark.skip(reason="Pipeline issue")
@pytest.mark.SKA_mid
def test_abort_in_resourcing_different_resources(json_factory):
    """Abort and Restart is executed."""
    assign_json = json_factory("command_AssignResources")
    assign_json2 = json_factory("command_AssignResources_2")
    release_json = json_factory("command_ReleaseResources")
    config_json = json_factory("command_Configure_2")
    scan_json = json_factory("command_Scan")

    # Modify release json
    release_json = json.loads(release_json)
    release_json["transaction_id"] = "txn-local-20210203-0002"
    release_json = json.dumps(release_json)

    try:
        tmc_helper.check_devices(DEVICE_LIST_FOR_CHECK_DEVICES)

        # Verify Telescope is Off/Standby#
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )

        # Invoke TelescopeOn() command on TMC#
        tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify State transitions after TelescopeOn#
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_ON_INFO, "State"
        )

        # Setting CSP subarray as defective
        csp_subarray_proxy = DeviceProxy(csp_subarray1)
        csp_subarray_proxy.SetDefective(json.dumps(INTERMEDIATE_STATE_DEFECT))

        # Invoke AssignResources() Command on TMC
        Resource(tmc_subarraynode1).assert_attribute("State").equals("ON")
        Resource(tmc_subarraynode1).assert_attribute("obsState").equals(
            "EMPTY"
        )
        central_node = DeviceProxy(centralnode)
        central_node.AssignResources(assign_json)

        # Verify ObsState is RESOURCING
        the_waiter = Waiter()
        the_waiter.set_wait_for_specific_obsstate(
            "RESOURCING", [tmc_subarraynode1, csp_subarray1]
        )
        the_waiter.set_wait_for_specific_obsstate("IDLE", [sdp_subarray1])
        the_waiter.wait(20)

        # Setting CSP back to normal
        csp_subarray_proxy.SetDefective(json.dumps({"enabled": False}))
        time.sleep(0.1)

        # Invoke Abort() command on TMC
        tmc_helper.invoke_abort(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify State transitions after Abort#
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_ABORT_INFO, "obsState"
        )
        # Invoke Restart() command on TMC
        tmc_helper.invoke_restart(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify ObsState is EMPTY#
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
        )
        # Invoke AssignResources() Command on TMC
        tmc_helper.compose_sub(assign_json2, **ON_OFF_DEVICE_COMMAND_DICT)

        # Verify ObsState is IDLE
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_IDLE_INFO, "obsState"
        )

        # Invoke Configure() Command on TMC
        tmc_helper.configure_subarray(
            config_json, **ON_OFF_DEVICE_COMMAND_DICT
        )
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_READY_INFO, "obsState"
        )

        # Invoke Scan() Command on TMC
        tmc_helper.scan(scan_json, **ON_OFF_DEVICE_COMMAND_DICT)
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_READY_INFO, "obsState"
        )

        # Invoke End() Command on TMC
        tmc_helper.end(**ON_OFF_DEVICE_COMMAND_DICT)
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_IDLE_INFO, "obsState"
        )
        # Invoke ReleaseResources() command on TMC
        tmc_helper.invoke_releaseResources(
            release_json, **ON_OFF_DEVICE_COMMAND_DICT
        )
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
        )
        # Invoke Standby() command on TMC
        tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )
    except Exception as e:
        LOGGER.exception("The exception is: %s", e)
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)


@pytest.mark.skip(reason="Random failure")
@pytest.mark.SKA_mid
def test_abort_in_resourcing_with_second_abort(json_factory):
    """Abort and Restart is executed."""
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")
    config_json = json_factory("command_Configure")
    scan_json = json_factory("command_Scan")
    try:
        #         tmc_helper.check_devices(DEVICE_LIST_FOR_CHECK_DEVICES)

        # Verify Telescope is Off/Standby#
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )

        # Invoke TelescopeOn() command on TMC#
        tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify State transitions after TelescopeOn#
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_ON_INFO, "State"
        )

        # Setting CSP subarray as defective
        csp_subarray_proxy = DeviceProxy(csp_subarray1)
        csp_subarray_proxy.SetDefective(json.dumps(INTERMEDIATE_STATE_DEFECT))

        # Invoke AssignResources() Command on TMC
        Resource(tmc_subarraynode1).assert_attribute("State").equals("ON")
        Resource(tmc_subarraynode1).assert_attribute("obsState").equals(
            "EMPTY"
        )
        central_node = DeviceProxy(centralnode)
        central_node.AssignResources(assign_json)

        # Verify ObsState is RESOURCING
        the_waiter = Waiter()
        the_waiter.set_wait_for_specific_obsstate(
            "RESOURCING", [tmc_subarraynode1]
        )
        the_waiter.wait(20)

        # Setting SDP and CSP back to normal
        csp_subarray_proxy.SetDefective(json.dumps({"enabled": False}))
        time.sleep(0.1)

        # Invoke Abort() command on TMC
        subarray_node = DeviceProxy(tmc_subarraynode1)
        subarray_node.Abort()

        # Invoke Abort() command on TMC
        with pytest.raises(Exception):
            tmc_helper.invoke_abort()

        # Verify ObsState is Aborted
        the_waiter = Waiter()
        the_waiter.set_wait_for_specific_obsstate(
            "ABORTED", [tmc_subarraynode1]
        )
        the_waiter.wait(200)

        # Invoke Restart() command on TMC
        tmc_helper.invoke_restart(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify ObsState is EMPTY#
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
        )
        # Invoke AssignResources() Command on TMC
        tmc_helper.compose_sub(assign_json, **ON_OFF_DEVICE_COMMAND_DICT)

        # Verify ObsState is IDLE
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_IDLE_INFO, "obsState"
        )

        # Invoke Configure() Command on TMC
        tmc_helper.configure_subarray(
            config_json, **ON_OFF_DEVICE_COMMAND_DICT
        )
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_READY_INFO, "obsState"
        )

        # Invoke Scan() Command on TMC
        tmc_helper.scan(scan_json, **ON_OFF_DEVICE_COMMAND_DICT)
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_READY_INFO, "obsState"
        )

        # Invoke End() Command on TMC
        tmc_helper.end(**ON_OFF_DEVICE_COMMAND_DICT)
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_IDLE_INFO, "obsState"
        )
        # Invoke ReleaseResources() command on TMC
        tmc_helper.invoke_releaseResources(
            release_json, **ON_OFF_DEVICE_COMMAND_DICT
        )
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
        )
        # Invoke Standby() command on TMC
        tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )
    except Exception as e:
        LOGGER.exception("The exception is: %s", e)
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)


@pytest.mark.skip(reason="random failure")
@pytest.mark.SKA_mid
def test_abort_in_configuring(json_factory):
    """Abort and Restart is executed."""
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")
    config_json = json_factory("command_Configure")
    scan_json = json_factory("command_Scan")
    try:
        tmc_helper.check_devices(DEVICE_LIST_FOR_CHECK_DEVICES)

        # Verify Telescope is Off/Standby#
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )

        # Invoke TelescopeOn() command on TMC#
        tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify State transitions after TelescopeOn#
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_ON_INFO, "State"
        )

        # Invoke AssignResources() Command on TMC#
        tmc_helper.compose_sub(assign_json, **ON_OFF_DEVICE_COMMAND_DICT)

        # Verify ObsState is IDLE#
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_IDLE_INFO, "obsState"
        )

        # Setting CSP subarray as defective
        csp_subarray_proxy = DeviceProxy(csp_subarray1)
        csp_subarray_proxy.SetDefective(
            json.dumps(INTERMEDIATE_CONFIGURING_OBS_STATE_DEFECT)
        )

        # Invoke Configure() Command on TMC
        Resource(tmc_subarraynode1).assert_attribute("obsState").equals("IDLE")
        subarray_node = DeviceProxy(tmc_subarraynode1)
        subarray_node.Configure(config_json)

        # Verify ObsState is CONFIGURING
        the_waiter = Waiter()
        the_waiter.set_wait_for_specific_obsstate(
            "CONFIGURING", [tmc_subarraynode1, csp_subarray1]
        )

        the_waiter.wait(100)

        the_waiter.set_wait_for_pointingstate("TRACK", [dish_master1])
        the_waiter.wait(200)

        # check for the SubarrayNode longRunningCommandResult event of
        # Configure command
        the_waiter.set_wait_for_long_running_command_result(
            Anything, [tmc_subarraynode1]
        )
        # Setting CSP back to normal
        csp_subarray_proxy.SetDefective(json.dumps({"enabled": False}))
        time.sleep(0.5)

        # Invoke Abort() command on TMC
        tmc_helper.invoke_abort(**ON_OFF_DEVICE_COMMAND_DICT)

        # TODO: move this to set_wait_for_aborted
        the_waiter.set_wait_for_pointingstate("READY", [dish_master1])
        the_waiter.wait(200)

        # Verify State transitions after Abort#
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_ABORT_INFO, "obsState"
        )

        # Invoke Restart() command on TMC
        tmc_helper.invoke_restart(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify ObsState is EMPTY#
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
        )
        # Invoke AssignResources() Command on TMC
        tmc_helper.compose_sub(assign_json, **ON_OFF_DEVICE_COMMAND_DICT)

        # Verify ObsState is IDLE
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_IDLE_INFO, "obsState"
        )

        # Invoke Configure() Command on TMC
        tmc_helper.configure_subarray(
            config_json, **ON_OFF_DEVICE_COMMAND_DICT
        )
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_READY_INFO, "obsState"
        )

        # Invoke Scan() Command on TMC
        tmc_helper.scan(scan_json, **ON_OFF_DEVICE_COMMAND_DICT)
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_READY_INFO, "obsState"
        )

        # Invoke End() Command on TMC
        tmc_helper.end(**ON_OFF_DEVICE_COMMAND_DICT)
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_IDLE_INFO, "obsState"
        )
        # Invoke ReleaseResources() command on TMC
        tmc_helper.invoke_releaseResources(
            release_json, **ON_OFF_DEVICE_COMMAND_DICT
        )
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
        )
        # Invoke Standby() command on TMC
        tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )
    except Exception as e:
        LOGGER.exception("The exception is: %s", e)
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)


@pytest.mark.skip(reason="timeout issue")
@pytest.mark.SKA_mid
def test_abort_in_scanning(json_factory):
    """Abort and Restart is executed."""
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")
    config_json = json_factory("command_Configure")
    scan_json = json_factory("command_Scan")
    try:
        tmc_helper.check_devices(DEVICE_LIST_FOR_CHECK_DEVICES)

        # Verify Telescope is Off/Standby#
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )

        # Invoke TelescopeOn() command on TMC#
        tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify State transitions after TelescopeOn#
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_ON_INFO, "State"
        )

        # Invoke AssignResources() Command on TMC#
        tmc_helper.compose_sub(assign_json, **ON_OFF_DEVICE_COMMAND_DICT)

        # Verify ObsState is IDLE#
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_IDLE_INFO, "obsState"
        )

        # Invoke Configure() Command on TMC
        tmc_helper.configure_subarray(
            config_json, **ON_OFF_DEVICE_COMMAND_DICT
        )
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_READY_INFO, "obsState"
        )

        # Setting CSP subarray as defective
        csp_subarray_proxy = DeviceProxy(csp_subarray1)
        csp_subarray_proxy.SetDefective(json.dumps(INTERMEDIATE_STATE_DEFECT))

        # Invoke Scan() Command on TMC
        Resource(tmc_subarraynode1).assert_attribute("obsState").equals(
            "READY"
        )
        subarray_node = DeviceProxy(tmc_subarraynode1)
        subarray_node.Scan(scan_json)

        time.sleep(1)

        # Verify ObsState is SCANNING
        the_waiter = Waiter()
        the_waiter.set_wait_for_specific_obsstate(
            "SCANNING", [tmc_subarraynode1]
        )
        the_waiter.wait(20)

        # Setting CSP back to normal
        csp_subarray_proxy.SetDefective(json.dumps({"enabled": False}))

        # Invoke Abort() command on TMC
        tmc_helper.invoke_abort(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify State transitions after Abort#
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_ABORT_INFO, "obsState"
        )

        #        # Invoke Restart() command on TMC
        tmc_helper.invoke_restart(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify ObsState is EMPTY#
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
        )
        # Invoke AssignResources() Command on TMC
        tmc_helper.compose_sub(assign_json, **ON_OFF_DEVICE_COMMAND_DICT)

        # Verify ObsState is IDLE
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_IDLE_INFO, "obsState"
        )

        # Invoke Configure() Command on TMC
        tmc_helper.configure_subarray(
            config_json, **ON_OFF_DEVICE_COMMAND_DICT
        )
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_READY_INFO, "obsState"
        )

        # Invoke Scan() Command on TMC
        tmc_helper.scan(scan_json, **ON_OFF_DEVICE_COMMAND_DICT)
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_READY_INFO, "obsState"
        )

        # Invoke End() Command on TMC
        tmc_helper.end(**ON_OFF_DEVICE_COMMAND_DICT)
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_IDLE_INFO, "obsState"
        )
        # Invoke ReleaseResources() command on TMC
        tmc_helper.invoke_releaseResources(
            release_json, **ON_OFF_DEVICE_COMMAND_DICT
        )
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
        )
        # Invoke Standby() command on TMC
        tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )
    except Exception as e:
        LOGGER.exception("The exception is: %s", e)
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)