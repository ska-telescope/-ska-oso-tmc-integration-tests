import pytest
from tango import DeviceProxy

from tests.conftest import LOGGER
from tests.resources.test_support.common_utils.common_helpers import (
    Waiter,
    resource,
)
from tests.resources.test_support.common_utils.tmc_helpers import TmcHelper
from tests.resources.test_support.constant import (
    DEVICE_LIST_FOR_CHECK_DEVICES,
    DEVICE_OBS_STATE_ABORT_INFO,
    DEVICE_OBS_STATE_EMPTY_INFO,
    DEVICE_OBS_STATE_IDLE_INFO,
    DEVICE_STATE_ON_INFO,
    DEVICE_STATE_STANDBY_INFO,
    ON_OFF_DEVICE_COMMAND_DICT,
    centralnode,
    tmc_subarraynode1,
)
from tests.resources.test_support.controls import check_subarray1_availability
from tests.resources.test_support.telescope_controls import (
    BaseTelescopeControl,
)
from tests.resources.test_support.tmc_helpers import tear_down


@pytest.mark.SKA_mid
def test_mid_abort_restart_in_restarting(json_factory):
    """Abort and Restart is executed."""
    telescope_control = BaseTelescopeControl()
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")
    tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)

    try:
        tmc_helper.check_devices(DEVICE_LIST_FOR_CHECK_DEVICES)

        # Verify Telescope is Off/Standby#
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )
        LOGGER.info("Staring up the Telescope")

        # Invoke TelescopeOn() command on TMC#
        tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)
        LOGGER.info("TelescopeOn command is invoked successfully")

        # Verify State transitions after TelescopeOn#
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_ON_INFO, "State"
        )

        # Check Subarray1 availability
        assert check_subarray1_availability(tmc_subarraynode1)

        # Invoke AssignResources() Command on TMC#
        tmc_helper.compose_sub(assign_json, **ON_OFF_DEVICE_COMMAND_DICT)
        LOGGER.info("AssignResources command is invoked successfully")

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
        subarray_node = DeviceProxy(tmc_subarraynode1)
        subarray_node.Restart()
        resource(tmc_subarraynode1).assert_attribute("obsState").equals(
            "RESTARTING"
        )

        # Invoke Abort() command on TMC
        with pytest.raises(Exception):
            tmc_helper.invoke_abort()

        # Verify ObsState is EMPTY
        the_waiter = Waiter()
        the_waiter.set_wait_for_specific_obsstate("EMPTY", [tmc_subarraynode1])
        the_waiter.wait(100)

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

    except Exception:
        tear_down(release_json)
