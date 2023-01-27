import pytest
import tests.resources.test_support.low.tmc_helpers as tmc
from tests.conftest import LOGGER
from tests.resources.test_support.low.sync_decorators import (
    sync_assign_resources,sync_configure,sync_end,sync_scan)
from tests.resources.test_support.constant_low import (
    DEVICE_STATE_STANDBY_INFO,
    DEVICE_STATE_ON_INFO,
    DEVICE_STATE_OFF_INFO,
    DEVICE_OBS_STATE_IDLE_INFO,
    DEVICE_OBS_STATE_EMPTY_INFO,
    DEVICE_OBS_STATE_READY_INFO,
)
from tests.resources.test_support.low.helpers import resource
from tests.resources.test_support.constant_low import tmc_subarraynode1, centralnode
from tango import DeviceProxy
from tests.resources.test_support.low.telescope_controls_low import TelescopeControlLow

@pytest.mark.MS
@pytest.mark.SKA_low
def test_scan_endscan_low(json_factory):
    """Scan and EndScan is executed."""
    try:
        telescope_control = TelescopeControlLow()
        assign_json = json_factory("command_assign_resource_low")
        release_json = json_factory("command_release_resource_low")
        configure_json = json_factory("command_Configure_low")
        scan_json = json_factory("command_scan_low")
        tmc.check_devices()
        fixture = {}
        fixture["state"] = "Unknown"

        """Verify Telescope is Off/Standby"""
        assert telescope_control.is_in_valid_state(DEVICE_STATE_STANDBY_INFO, "State")
        LOGGER.info("Staring up the Telescope")

        """Invoke TelescopeOn() command on TMC"""
        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
        tmc.set_to_on()
        LOGGER.info("TelescopeOn command is invoked successfully")

        """Verify State transitions after TelescopeOn"""
        assert telescope_control.is_in_valid_state(DEVICE_STATE_ON_INFO, "State")
        fixture["state"] = "TelescopeOn"

        """Invoke AssignResources() Command on TMC"""
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")
        @sync_assign_resources()
        def compose_sub():
            resource(tmc_subarraynode1).assert_attribute("State").equals(
                "ON"
            )
            resource(tmc_subarraynode1).assert_attribute("obsState").equals(
                "EMPTY"
            )
            central_node = DeviceProxy(centralnode)
            tmc.check_devices()
            central_node.AssignResources(assign_json)
            LOGGER.info("Invoked AssignResources on CentralNode")

        compose_sub()

        LOGGER.info("AssignResources command is invoked successfully")

        """Verify ObsState is Idle"""
        assert telescope_control.is_in_valid_state(DEVICE_OBS_STATE_IDLE_INFO, "obsState")
        fixture["state"] ="AssignResources"

        """Invoke Configure() Command on TMC"""
        LOGGER.info("Invoking Configure command on TMC CentralNode")
        @sync_configure()
        def configure_subarray():
            resource(tmc_subarraynode1).assert_attribute("obsState").equals(
                "IDLE"
            )
            subarray_node = DeviceProxy(tmc_subarraynode1)
            subarray_node.Configure(configure_json)
            LOGGER.info("Invoked Configure on SubarrayNode")

        configure_subarray()

        """Verify ObsState is READY"""
        assert telescope_control.is_in_valid_state(DEVICE_OBS_STATE_READY_INFO, "obsState")
        fixture["state"] ="Configure"
        LOGGER.info("Configure command is invoked successfully")

        """Invoke Scan() Command on TMC"""
        LOGGER.info("Invoking Scan command on TMC SubarrayNode")
        @sync_scan()
        def scan():
            resource(tmc_subarraynode1).assert_attribute("obsState").equals(
                "READY"
            )
            subarray_node = DeviceProxy(tmc_subarraynode1)
            subarray_node.Scan(scan_json)
            LOGGER.info("Invoked Scan on SubarrayNode")

        scan()

        """Verify ObsState is READY"""
        assert telescope_control.is_in_valid_state(DEVICE_OBS_STATE_READY_INFO, "obsState")
        fixture["state"] ="Scan"
        LOGGER.info("Scan command is invoked successfully")

        """Invoke End() Command on TMC"""
        LOGGER.info("Invoking End command on TMC SubarrayNode")
        @sync_end()
        def end():
            resource(tmc_subarraynode1).assert_attribute("obsState").equals(
                "READY"
            )
            subarray_node = DeviceProxy(tmc_subarraynode1)
            subarray_node.End()
            LOGGER.info("Invoked End on SubarrayNode")

        end()

        """Verify ObsState is IDLE"""
        assert telescope_control.is_in_valid_state(DEVICE_OBS_STATE_IDLE_INFO, "obsState")
        fixture["state"] ="End"
        LOGGER.info("End command is invoked successfully")

        """Invoke ReleaseResources() command on TMC"""
        tmc.invoke_releaseResources(release_json)

        fixture["state"] = "ReleaseResources"
        assert telescope_control.is_in_valid_state(DEVICE_OBS_STATE_EMPTY_INFO, "obsState")

        """Invoke TelescopeOff() command on TMC"""
        tmc.set_to_off()

        """Verify State transitions after TelescopeOff"""
        assert telescope_control.is_in_valid_state(DEVICE_STATE_OFF_INFO, "State")
        fixture["state"] = "TelescopeOff"

        LOGGER.info("Tests complete.")

    except:
        if fixture["state"] == "AssignResources":
            tmc.invoke_releaseResources(release_json)
        if fixture["state"] == "Configure":
            tmc.end()
            tmc.invoke_releaseResources(release_json)
        if fixture["state"] == "Scan":
            tmc.end()
            tmc.invoke_releaseResources(release_json)
        if fixture["state"] == "TelescopeOn":
            tmc.set_to_off()
        raise