import pytest

from tests.conftest import LOGGER
from tests.resources.test_support.common_utils.tmc_helpers import TmcHelper
from tests.resources.test_support.constant import (
    DEVICE_LIST_FOR_CHECK_DEVICES,
    DEVICE_OBS_STATE_EMPTY_INFO,
    DEVICE_OBS_STATE_IDLE_INFO,
    DEVICE_OBS_STATE_READY_INFO,
    DEVICE_STATE_ON_INFO,
    DEVICE_STATE_STANDBY_INFO,
    ON_OFF_DEVICE_COMMAND_DICT,
    centralnode,
    tmc_subarraynode1,
)
from tests.resources.test_support.telescope_controls import (
    BaseTelescopeControl,
)
from tests.resources.test_support.tmc_helpers import tear_down


@pytest.mark.SKA_mid
@pytest.mark.MS
def test_successive_scan_with_different_configurations(json_factory):
    """Successive Scan command with different configurations."""
    telescope_control = BaseTelescopeControl()
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")
    configure_json = json_factory("command_Configure")
    configure_json_2 = json_factory("command_Configure_2")
    configure_json_3 = json_factory("command_Configure_3")
    scan_json = json_factory("command_Scan")
    scan_json_2 = json_factory("command_Scan_2")
    scan_json_3 = json_factory("command_Scan_3")
    tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)

    try:
        tmc_helper.check_devices(DEVICE_LIST_FOR_CHECK_DEVICES)

        # Verify Telescope is Off/Standby#
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )
        LOGGER.info("Staring up the Telescope")

        # Invoke TelescopeOn() command on TMC#
        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
        tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)
        LOGGER.info("TelescopeOn command is invoked successfully")

        # Verify State transitions after TelescopeOn#
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_ON_INFO, "State"
        )

        # Invoke AssignResources() Command on TMC#
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")
        tmc_helper.compose_sub(assign_json, **ON_OFF_DEVICE_COMMAND_DICT)
        LOGGER.info("AssignResources command is invoked successfully")

        # Verify ObsState is IDLE#
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_IDLE_INFO, "obsState"
        )

        # Invoke Configure() Command on TMC#
        LOGGER.info("Invoking Configure command on TMC SubarrayNode")
        tmc_helper.configure_subarray(
            configure_json, **ON_OFF_DEVICE_COMMAND_DICT
        )

        # Verify ObsState is READY#
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_READY_INFO, "obsState"
        )

        # Invoke Scan() command on TMC#
        tmc_helper.scan(scan_json, **ON_OFF_DEVICE_COMMAND_DICT)

        # Verify ObsState is READY#
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_READY_INFO, "obsState"
        )

        # Invoke Configure() Command on TMC#
        LOGGER.info("Invoking Configure command on TMC SubarrayNode")
        tmc_helper.configure_subarray(
            configure_json_2, **ON_OFF_DEVICE_COMMAND_DICT
        )

        # Verify ObsState is READY#
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_READY_INFO, "obsState"
        )

        # Invoke Scan() command on TMC#
        tmc_helper.scan(scan_json_2, **ON_OFF_DEVICE_COMMAND_DICT)

        # Verify ObsState is READY#
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_READY_INFO, "obsState"
        )

        # Verify ObsState is READY#
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_READY_INFO, "obsState"
        )

        # Invoke Configure() Command on TMC#
        LOGGER.info("Invoking Configure command on TMC SubarrayNode")
        tmc_helper.configure_subarray(
            configure_json_3, **ON_OFF_DEVICE_COMMAND_DICT
        )

        # Invoke Scan() command on TMC#
        tmc_helper.scan(scan_json_3, **ON_OFF_DEVICE_COMMAND_DICT)

        # Verify ObsState is READY#
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_READY_INFO, "obsState"
        )

        # Invoke End() command on TMC#
        tmc_helper.end(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify ObsState is IDLE#
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_IDLE_INFO, "obsState"
        )

        # Invoke ReleaseResources() Command on TMC#
        LOGGER.info("Invoking ReleaseResources command on TMC CentralNode")
        tmc_helper.invoke_releaseResources(
            release_json, **ON_OFF_DEVICE_COMMAND_DICT
        )
        LOGGER.info("ReleaseResources command is invoked successfully")

        # Verify ObsState is EMPTY#
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
        )

        # Invoke TelescopeStandby() command on TMC#
        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
        tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)
        LOGGER.info("TelescopeStandby command is invoked successfully")

        # Verify State transitions after TelescopeStandby#
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )

        LOGGER.info("Test complete.")

    except Exception:
        tear_down(release_json)


@pytest.mark.SKA_mid
def test_successive_scan_with_same_configurations(json_factory):
    """Successive Scan command with same configurations."""
    telescope_control = BaseTelescopeControl()
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")
    configure_json = json_factory("command_Configure")
    scan_json = json_factory("command_Scan")
    scan_json_2 = json_factory("command_Scan_2")
    scan_json_3 = json_factory("command_Scan_3")
    tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)

    try:
        tmc_helper.check_devices(DEVICE_LIST_FOR_CHECK_DEVICES)

        # Verify Telescope is Off/Standby#
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )
        LOGGER.info("Staring up the Telescope")

        # Invoke TelescopeOn() command on TMC#
        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
        tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)
        LOGGER.info("TelescopeOn command is invoked successfully")

        # Verify State transitions after TelescopeOn#
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_ON_INFO, "State"
        )

        # Invoke AssignResources() Command on TMC#
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")
        tmc_helper.compose_sub(assign_json, **ON_OFF_DEVICE_COMMAND_DICT)
        LOGGER.info("AssignResources command is invoked successfully")

        # Verify ObsState is IDLE#
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_IDLE_INFO, "obsState"
        )

        # Invoke Configure() Command on TMC#
        LOGGER.info("Invoking Configure command on TMC SubarrayNode")
        tmc_helper.configure_subarray(
            configure_json, **ON_OFF_DEVICE_COMMAND_DICT
        )

        # Verify ObsState is READY#
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_READY_INFO, "obsState"
        )

        # Invoke Scan() command on TMC#
        tmc_helper.scan(scan_json, **ON_OFF_DEVICE_COMMAND_DICT)

        # Verify ObsState is READY#
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_READY_INFO, "obsState"
        )

        # Invoke Scan() command on TMC#
        tmc_helper.scan(scan_json_2, **ON_OFF_DEVICE_COMMAND_DICT)

        # Verify ObsState is READY#
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_READY_INFO, "obsState"
        )

        # Invoke Scan() command on TMC#
        tmc_helper.scan(scan_json_3, **ON_OFF_DEVICE_COMMAND_DICT)

        # Verify ObsState is READY#
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_READY_INFO, "obsState"
        )

        # Invoke End() command on TMC#
        tmc_helper.end(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify ObsState is IDLE#
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_IDLE_INFO, "obsState"
        )

        # Invoke ReleaseResources() Command on TMC#
        LOGGER.info("Invoking ReleaseResources command on TMC CentralNode")
        tmc_helper.invoke_releaseResources(
            release_json, **ON_OFF_DEVICE_COMMAND_DICT
        )
        LOGGER.info("ReleaseResources command is invoked successfully")

        # Verify ObsState is EMPTY#
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
        )

        # Invoke TelescopeStandby() command on TMC#
        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
        tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)
        LOGGER.info("TelescopeStandby command is invoked successfully")

        # Verify State transitions after TelescopeStandby#
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )

        LOGGER.info("Test complete.")

    except Exception:
        tear_down(release_json)
