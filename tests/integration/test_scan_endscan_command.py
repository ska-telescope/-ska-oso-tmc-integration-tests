import pytest
from tests.resources.test_support.controls import telescope_is_in_standby_state ,telescope_is_in_on_state ,subarray_obs_state_is_idle ,subarray_obs_state_is_ready, subarray_obs_state_is_empty, telescope_is_in_off_state
import tests.resources.test_support.tmc_helpers as tmc
from tests.conftest import LOGGER

assign_resources_file = "command_AssignResources.json"
release_resources_file  = "command_ReleaseResources.json"
configure_resources_file = "command_Configure.json"
scan_file= "command_Scan.json"

@pytest.mark.SKA_mid
def test_scan_endscan():
    """Scan and EndScan is executed."""
    try:
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
        assign_res_input = tmc.get_input_str(assign_resources_file)
        tmc.compose_sub(assign_res_input)

        """Verify ObsState is Idle"""
        assert subarray_obs_state_is_idle()
        fixture["state"] ="AssignResources"

        """Invoke Configure() Command on TMC"""
        LOGGER.info("Invoking Configure command on TMC CentralNode")
        configure_input_str = tmc.get_input_str(configure_resources_file)
        tmc.configure_subarray(configure_input_str)

        """Verify ObsState is READY"""
        assert subarray_obs_state_is_ready()
        fixture["state"] ="Configure"

        """Invoke Scan() Command on TMC"""
        LOGGER.info("Invoking Scan command on TMC CentralNode")
        scan_input = tmc.get_input_str(scan_file)
        tmc.scan(scan_input)

        """Verify ObsState is READY"""
        assert subarray_obs_state_is_ready()
        fixture["state"] ="Scan"

        """Invoke End() Command on TMC"""
        LOGGER.info("Invoking End command on TMC SubarrayNode")
        tmc.end()

        """Verify ObsState is IDLE"""
        assert subarray_obs_state_is_idle()
        fixture["state"] ="End"

        """Invoke ReleaseResources() command on TMC"""
        release_input_str = tmc.get_input_str(release_resources_file)
        tmc.invoke_releaseResources(release_input_str)

        fixture["state"] = "ReleaseResources"
        assert subarray_obs_state_is_empty()

        """Invoke TelescopeOff() command on TMC"""
        tmc.set_to_off()

        """Verify State transitions after TelescopeOff"""
        assert telescope_is_in_off_state()
        fixture["state"] = "TelescopeOff"

    except:
        if fixture["state"] == "AssignResources":
            tmc.invoke_releaseResources(release_input_str)
        if fixture["state"] == "Configure":
            tmc.end()
            tmc.invoke_releaseResources(release_input_str)
        if fixture["state"] == "Scan":
            tmc.end()
            tmc.invoke_releaseResources(release_input_str)
        if fixture["state"] == "TelescopeOn":
            tmc.set_to_off()
        raise