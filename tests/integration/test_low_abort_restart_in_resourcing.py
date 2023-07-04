import time

import pytest
from tango import DeviceProxy

from tests.conftest import LOGGER
from tests.resources.test_support.common_utils.common_helpers import resource
from tests.resources.test_support.common_utils.tmc_helpers import TmcHelper
from tests.resources.test_support.constant_low import (
    DEVICE_LIST_FOR_CHECK_DEVICES,
    DEVICE_OBS_STATE_ABORT_INFO,
    DEVICE_OBS_STATE_EMPTY_INFO,
    DEVICE_STATE_OFF_INFO,
    DEVICE_STATE_ON_INFO,
    DEVICE_STATE_STANDBY_INFO,
    ON_OFF_DEVICE_COMMAND_DICT,
    centralnode,
    csp_subarray1,
    tmc_subarraynode1,
)
from tests.resources.test_support.controls import check_subarray1_availability
from tests.resources.test_support.low.telescope_controls_low import (
    TelescopeControlLow,
)


@pytest.mark.skip(
    reason="Abort command is not implemented on SDP Subarray Leaf Node."
)
@pytest.mark.SKA_low
def test_low_abort_restart_in_resourcing(json_factory):
    """Abort and Restart is executed."""
    telescope_control = TelescopeControlLow()
    assign_json = json_factory("command_assign_resource_low")
    release_json = json_factory("command_release_resource_low")
    fixture = {}
    fixture["state"] = "Unknown"
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
        fixture["state"] = "TelescopeOn"

        # Check Subarray1 availability
        assert check_subarray1_availability(tmc_subarraynode1)

        # Setting CSP to defective
        csp_subarray_proxy = DeviceProxy(csp_subarray1)
        csp_subarray_proxy.SetDefective(True)

        # Invoke AssignResources() Command on TMC#
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")

        resource(tmc_subarraynode1).assert_attribute("State").equals("ON")
        resource(tmc_subarraynode1).assert_attribute("obsState").equals(
            "EMPTY"
        )
        central_node = DeviceProxy(centralnode)
        central_node.AssignResources(assign_json)
        LOGGER.info("Invoked AssignResources on CentralNode")

        # Verify ObsState is RESOURCING
        time.sleep(1)
        resource(tmc_subarraynode1).assert_attribute("obsState").equals(
            "RESOURCING"
        )

        # Setting CSP back to normal
        csp_subarray_proxy.SetDefective(False)

        # Invoke Abort() command on TMC#
        tmc_helper.invoke_abort(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify State transitions after Abort#
        fixture["state"] = "Abort"
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_ABORT_INFO, "obsState"
        )

        # Invoke Restart() command on TMC#
        tmc_helper.invoke_restart(**ON_OFF_DEVICE_COMMAND_DICT)

        fixture["state"] = "Restart"
        # Verify ObsState is EMPTY#
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
        )

        # Invoke TelescopeOff() command on TMC#
        tmc_helper.set_to_off(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify State transitions after TelescopeOff#
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_OFF_INFO, "State"
        )
        fixture["state"] = "TelescopeOff"

        LOGGER.info("Test complete.")

    except Exception:
        if fixture["state"] == "AssignResources":
            tmc_helper.invoke_releaseResources(
                release_json, **ON_OFF_DEVICE_COMMAND_DICT
            )
        if fixture["state"] == "TelescopeOn":
            tmc_helper.set_to_off(**ON_OFF_DEVICE_COMMAND_DICT)
        raise
