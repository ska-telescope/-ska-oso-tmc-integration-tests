import pytest
import json
from tests.resources.test_support.controls import telescope_is_in_standby_state, telescope_is_in_on_state, telescope_is_in_off_state, subarray_obs_state_is_empty, subarray_obs_state_is_idle
import tests.resources.test_support.tmc_helpers as tmc
from tests.conftest import LOGGER
from tests.resources.test_support.sync_decorators import sync_assign_resources
from tests.resources.test_support.helpers import resource
from tango import DeviceProxy
from tests.resources.test_support.constant import (
    tmc_subarraynode1, centralnode)


@pytest.mark.SKA_mid
def test_assign_invalid_json(json_factory):
    try:
        """AssignResources and ReleaseResources is executed."""
        assign_json = json_factory("command_invalid_assign_release")
        tmc.check_devices()
        fixture = {}
        fixture["state"] = "Unknown"

        """Verify Telescope is Off/Standby"""
        assert telescope_is_in_standby_state()
        LOGGER.info("Staring up the Telescope")

        """Invoke TelescopeOn() command on TMC"""
        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
        tmc.set_to_on()
        LOGGER.info("TelescopeOn command is invoked successfully")

        """Verify State transitions after TelescopeOn"""
        assert telescope_is_in_on_state()
        fixture["state"] = "TelescopeOn"

        """Invoke AssignResources() Command on TMC"""
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")
        resource( tmc_subarraynode1).assert_attribute("State").equals(
            "ON"
        )
        resource(tmc_subarraynode1).assert_attribute("obsState").equals(
            "EMPTY"
        )
        central_node = DeviceProxy(centralnode)
        tmc.check_devices()
        ret_code, message = central_node.AssignResources(json.dumps(assign_json))

        #Assert with TaskStatus as REJECTED
        assert ret_code == 5
        LOGGER.info(message)

        """Verify ObsState is EMPTY"""
        assert subarray_obs_state_is_empty()

        # """Invoke TelescopeOff() command on TMC"""
        tmc.set_to_off()

        # """Verify State transitions after TelescopeOff"""
        assert telescope_is_in_off_state()
        fixture["state"] = "TelescopeOff"

        # LOGGER.info("Tests complete.")
    except:
        LOGGER.info("Exception occurred in the test for state = {}".format(fixture["state"]))
        LOGGER.info("Tearing down...")
        if fixture["state"] == "TelescopeOn":
            tmc.set_to_off()
        raise

@pytest.mark.SKA_mid
def test_release_invalid_json(json_factory):
    try:
        """AssignResources and ReleaseResources is executed."""

        assign_json = json_factory("command_AssignResources")
        release_json = json_factory("command_ReleaseResources")
        invalid_release_json = json_factory("command_invalid_assign_release")
        tmc.check_devices()
        fixture = {}
        fixture["state"] = "Unknown"

        """Verify Telescope is Off/Standby"""
        assert telescope_is_in_standby_state()
        LOGGER.info("Staring up the Telescope")

        """Invoke TelescopeOn() command on TMC"""
        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
        tmc.set_to_on()
        LOGGER.info("TelescopeOn command is invoked successfully")

        """Verify State transitions after TelescopeOn"""
        assert telescope_is_in_on_state()
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
            central_node.AssignResources(json.dumps(assign_json))
            LOGGER.info("Invoked AssignResources on CentralNode")

        compose_sub()

        LOGGER.info("AssignResources command is invoked successfully")

        """Verify ObsState is Idle"""
        assert subarray_obs_state_is_idle()
        fixture["state"] ="AssignResources"

        """Invoke ReleaseResources() command on TMC"""
        central_node = DeviceProxy(centralnode)
        ret_code, message=central_node.ReleaseResources(json.dumps(invalid_release_json))
        #Assert with TaskStatus as REJECTED
        assert ret_code == 5
        LOGGER.info(message)
        # Check if telescope is in previous state
        fixture["state"] = "ReleaseResources"
        assert subarray_obs_state_is_idle()
        #Invoke release resources
        """Invoke ReleaseResources() command on TMC"""
        tmc.invoke_releaseResources(json.dumps(release_json))

        fixture["state"] = "ReleaseResources"
        assert subarray_obs_state_is_empty()

        """Invoke TelescopeOff() command on TMC"""
        tmc.set_to_off()

        """Verify State transitions after TelescopeOff"""
        assert telescope_is_in_off_state()
        fixture["state"] = "TelescopeOff"

        LOGGER.info("Tests complete.")

    except:
        if fixture["state"] == "AssignResources":
            tmc.invoke_releaseResources(json.dumps(release_json))
        if fixture["state"] == "TelescopeOn":
            tmc.set_to_off()
        raise
