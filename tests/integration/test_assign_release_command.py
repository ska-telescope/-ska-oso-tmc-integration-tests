import pytest
from tango import DeviceProxy, EventType

import tests.resources.test_support.tmc_helpers as tmc
from tests.conftest import LOGGER
from tests.resources.test_support.common_utils.result_code import ResultCode
from tests.resources.test_support.common_utils.tmc_helpers import TmcHelper
from tests.resources.test_support.constant import (
    DEVICE_HEALTH_STATE_OK_INFO,
    DEVICE_STATE_ON_INFO,
    DEVICE_STATE_STANDBY_INFO,
    ON_OFF_DEVICE_COMMAND_DICT,
    centralnode,
    csp_subarray1,
    tmc_subarraynode1,
)
from tests.resources.test_support.controls import (
    subarray_obs_state_is_empty,
    subarray_obs_state_is_idle,
    telescope_is_in_on_state,
    telescope_is_in_standby_state,
)
from tests.resources.test_support.helpers import resource
from tests.resources.test_support.mid.telescope_controls_mid import (
    TelescopeControlMid,
)
from tests.resources.test_support.sync_decorators import sync_assign_resources
from tests.resources.test_support.telescope_controls import (
    BaseTelescopeControl,
)
from tests.resources.test_support.tmc_helpers import tear_down


@pytest.mark.SKA_mid
def test_assign_release(json_factory):
    """AssignResources and ReleaseResources is executed."""
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")
    try:
        tmc.check_devices()

        # Verify Telescope is Off/Standby
        assert telescope_is_in_standby_state()
        LOGGER.info("Staring up the Telescope")

        # Invoke TelescopeOn() command on TMC
        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
        tmc.set_to_on()
        LOGGER.info("TelescopeOn command is invoked successfully")

        # Verify State transitions after TelescopeOn
        assert telescope_is_in_on_state()

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
        assert subarray_obs_state_is_idle()

        # Invoke ReleaseResources() command on TMC
        tmc.invoke_releaseResources(release_json)

        assert subarray_obs_state_is_empty()

        # Invoke TelescopeStandby() command on TMC
        tmc.set_to_standby()

        # Verify State transitions after TelescopeStandby
        assert telescope_is_in_standby_state()

        LOGGER.info("Tests complete.")

    except Exception:
        tear_down(release_json)


@pytest.mark.assignme
@pytest.mark.SKA_mid
def test_assign_release_timeout(json_factory, change_event_callbacks):
    """AssignResources and ReleaseResources is executed."""
    assign_json = json_factory("command_assign_resource_low")
    release_json = json_factory("command_release_resource_low")
    try:
        telescope_control = TelescopeControlMid()
        tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)

        fixture = {}
        fixture["state"] = "Unknown"

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
        result, unique_id = tmc_helper.compose_sub(
            assign_json, **ON_OFF_DEVICE_COMMAND_DICT
        )

        assert result[0].endswith("AssignResources")
        assert result[0] == ResultCode.QUEUED

        change_event_callbacks["longRunningCommandResult"].assert_change_event(
            (unique_id[0], "Timeout has occured, command failed"),
            lookahead=4,
        )
        csp_subarray.SetDefective(False)
    except Exception:
        tear_down(release_json)


@pytest.mark.SKA_mid
def test_health_check_mid():
    telescope_control = BaseTelescopeControl()
    assert telescope_control.is_in_valid_state(
        DEVICE_HEALTH_STATE_OK_INFO, "healthState"
    )
