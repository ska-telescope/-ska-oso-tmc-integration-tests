import pytest
from tango import DeviceProxy

import tests.resources.test_support.low.tmc_helpers as tmc
from tests.conftest import LOGGER
from tests.resources.test_support.constant_low import (
    DEVICE_HEALTH_STATE_OK_INFO,
    DEVICE_OBS_STATE_EMPTY_INFO,
    DEVICE_OBS_STATE_IDLE_INFO,
    DEVICE_STATE_OFF_INFO,
    DEVICE_STATE_ON_INFO,
    DEVICE_STATE_STANDBY_INFO,
    centralnode,
    tmc_subarraynode1,
)
from tests.resources.test_support.low.helpers import resource
from tests.resources.test_support.low.sync_decorators import (
    sync_assign_resources,
)
from tests.resources.test_support.low.telescope_controls_low import (
    TelescopeControlLow,
)


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
        tmc.invoke_releaseResources(release_json)

        fixture["state"] = "ReleaseResources"
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
        )

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


@pytest.mark.SKA_low
def test_health_check_low():
    telescope_control = TelescopeControlLow()
    assert telescope_control.is_in_valid_state(
        DEVICE_HEALTH_STATE_OK_INFO, "healthState"
    )
