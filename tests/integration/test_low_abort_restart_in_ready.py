import pytest
from tango import DeviceProxy
from tests.resources.test_support.constant_low import (centralnode, tmc_subarraynode1, DEVICE_LIST_FOR_CHECK_DEVICES,
DEVICE_STATE_STANDBY_INFO, ON_OFF_DEVICE_COMMAND_DICT, DEVICE_STATE_ON_INFO, DEVICE_OBS_STATE_IDLE_INFO,
csp_subarray1, DEVICE_OBS_STATE_ABORT_INFO, DEVICE_OBS_STATE_EMPTY_INFO, DEVICE_STATE_OFF_INFO, DEVICE_OBS_STATE_READY_INFO)
from tests.resources.test_support.low.telescope_controls_low import TelescopeControlLow
from tests.resources.test_support.common_utils.tmc_helpers import TmcHelper                                                               
from tests.conftest import LOGGER

@pytest.mark.SKA_low
def test_low_abort_restart_in_ready(json_factory):
    """Abort and Restart is executed."""
    telescope_control = TelescopeControlLow()
    assign_json = json_factory("command_assign_resource_low")
    release_json = json_factory("command_release_resource_low")
    configure_json = json_factory("command_Configure_low")
    fixture = {}
    fixture["state"] = "Unknown"
    tmc_helper=TmcHelper(centralnode, tmc_subarraynode1)
    
    try:
        tmc_helper.check_devices(DEVICE_LIST_FOR_CHECK_DEVICES)

        # Verify Telescope is Off/Standby# 
        assert telescope_control.is_in_valid_state(DEVICE_STATE_STANDBY_INFO, "State")
        LOGGER.info("Staring up the Telescope")

        # Invoke TelescopeOn() command on TMC# 
        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
        tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)
        LOGGER.info("TelescopeOn command is invoked successfully")

        # Verify State transitions after TelescopeOn# 
        assert telescope_control.is_in_valid_state(DEVICE_STATE_ON_INFO, "State")
        fixture["state"] = "TelescopeOn"

        # Invoke AssignResources() Command on TMC# 
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")
        tmc_helper.compose_sub(assign_json,**ON_OFF_DEVICE_COMMAND_DICT)
        LOGGER.info("AssignResources command is invoked successfully")

        # Verify ObsState is IDLE# 
        assert telescope_control.is_in_valid_state(DEVICE_OBS_STATE_IDLE_INFO, "obsState")
        fixture["state"] ="AssignResources"

        # Invoke Configure() Command on TMC# 
        LOGGER.info("Invoking Configure command on TMC SubarrayNode")
        tmc_helper.configure_subarray(configure_json,**ON_OFF_DEVICE_COMMAND_DICT)
        
        # Verify ObsState is READY# 
        assert telescope_control.is_in_valid_state(DEVICE_OBS_STATE_READY_INFO, "obsState")
        fixture["state"] = "Configure"

        # Invoke Abort() command on TMC#  
        tmc_helper.invoke_abort(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify State transitions after Abort# 
        fixture["state"] = "Abort"
        assert telescope_control.is_in_valid_state(DEVICE_OBS_STATE_ABORT_INFO, "obsState")

        # Invoke Restart() command on TMC# 
        tmc_helper.invoke_restart(**ON_OFF_DEVICE_COMMAND_DICT)

        fixture["state"] = "Restart"
        # Verify ObsState is EMPTY# 
        assert telescope_control.is_in_valid_state(DEVICE_OBS_STATE_EMPTY_INFO, "obsState")

        # Invoke TelescopeOff() command on TMC# 
        tmc_helper.set_to_off(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify State transitions after TelescopeOff# 
        assert telescope_control.is_in_valid_state(DEVICE_STATE_OFF_INFO, "State")
        fixture["state"] = "TelescopeOff"

        LOGGER.info("Test complete.")

    except:
        if fixture["state"] == "AssignResources":
            tmc_helper.invoke_releaseResources(release_json,**ON_OFF_DEVICE_COMMAND_DICT)
        if fixture["state"] == "TelescopeOn":
            tmc_helper.set_to_off(**ON_OFF_DEVICE_COMMAND_DICT)
        raise
        