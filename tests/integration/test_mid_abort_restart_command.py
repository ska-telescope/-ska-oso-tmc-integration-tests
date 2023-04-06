import pytest
import time
from tango import DeviceProxy
from tests.resources.test_support.controls import (
    telescope_is_in_on_state,
    telescope_is_in_off_state,
    subarray_obs_state_is_idle,
    subarray_obs_state_is_aborted,
    subarray_obs_state_is_empty,
    subarray_obs_state_is_ready,
)
import tests.resources.test_support.tmc_helpers as tmc
from tests.resources.test_support.constant import (
    centralnode,
    tmc_subarraynode1,
    sdp_subarray1,
)
from tests.resources.test_support.helpers import resource
from tests.conftest import LOGGER

@pytest.mark.SKA_mid
@pytest.mark.Abort
def test_abort_restart(json_factory):
    """Abort and Restart is executed."""
    fixture = {}
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")
    try:
        tmc.check_devices()
        fixture["state"] = "Unknown"

        # Verify Telescope is Off/Standby
        assert telescope_is_in_off_state()
        LOGGER.info("Staring up the Telescope")

        # Invoke TelescopeOn() command on TMC
        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
        tmc.set_to_on()
        LOGGER.info("TelescopeOn command is invoked successfully")

        # Verify State transitions after TelescopeOn
        assert telescope_is_in_on_state()
        fixture["state"] = "TelescopeOn"

        # Invoke AssignResources() Command on TMC
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")
        tmc.compose_sub(assign_json)
        LOGGER.info("AssignResources command is invoked successfully")

        # Verify ObsState is IDLE
        assert subarray_obs_state_is_idle()
        fixture["state"] ="AssignResources"

        # Invoke Abort() command on TMC
        tmc.invoke_abort()

        fixture["state"] = "Abort"
        assert subarray_obs_state_is_aborted()

        # Invoke Restart() command on TMC
        tmc.invoke_restart()

        fixture["state"] = "Restart"
        # Verify ObsState is EMPTY
        assert subarray_obs_state_is_empty()

        # Invoke TelescopeOff() command on TMC
        tmc.set_to_off()

        # Verify State transitions after TelescopeOff
        assert telescope_is_in_off_state()
        fixture["state"] = "TelescopeOff"

        LOGGER.info("Tests complete.")

    except:
        if fixture["state"] == "AssignResources":
            tmc.invoke_releaseResources(release_json)
        if fixture["state"] == "TelescopeOn":
            tmc.set_to_off()
        raise


@pytest.mark.SKA_mid
@pytest.mark.Abort
def test_abort_in_empty():
    """Abort and Restart is executed."""
    fixture = {}
    try:
        tmc.check_devices()
        fixture["state"] = "Unknown"

        # Verify Telescope is Off/Standby
        assert telescope_is_in_off_state()
        LOGGER.info("Staring up the Telescope")

        # Invoke TelescopeOn() command on TMC
        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
        tmc.set_to_on()
        LOGGER.info("TelescopeOn command is invoked successfully")

        # Verify State transitions after TelescopeOn
        assert telescope_is_in_on_state()
        fixture["state"] = "TelescopeOn"

        # Verify ObsState is EMPTY
        assert subarray_obs_state_is_empty()

        # Invoke Abort() command on TMC
        with pytest.raises(Exception):
            tmc.invoke_abort()

        # Invoke TelescopeOff() command on TMC
        tmc.set_to_off()

        # Verify State transitions after TelescopeOff
        assert telescope_is_in_off_state()
        fixture["state"] = "TelescopeOff"

        LOGGER.info("Tests complete.")

    except:
        if fixture["state"] == "TelescopeOn":
            tmc.set_to_off()
        raise


@pytest.mark.SKA_mid
@pytest.mark.Abort
def test_abort_in_resourcing(json_factory):
    """Abort and Restart is executed."""
    fixture = {}
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")
    config_json = json_factory("command_Configure")
    scan_json = json_factory("command_Scan")
    try:
        tmc.check_devices()
        fixture["state"] = "Unknown"

        # Verify Telescope is Off/Standby
        assert telescope_is_in_off_state()
        LOGGER.info("Staring up the Telescope")

        # Invoke TelescopeOn() command on TMC
        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
        tmc.set_to_on()
        LOGGER.info("TelescopeOn command is invoked successfully")

        # Verify State transitions after TelescopeOn
        assert telescope_is_in_on_state()
        fixture["state"] = "TelescopeOn"

        # Setting SDP subarray as defective
        sdp_subarray_proxy = DeviceProxy(sdp_subarray1)
        sdp_subarray_proxy.SetDefective(True)

        # Invoke AssignResources() Command on TMC
        tmc.compose_sub(assign_json)

        # Verify ObsState is RESOURCING
        time.sleep(0.1)
        resource(tmc_subarraynode1).assert_attribute("obsState").equals("RESOURCING")

        # Setting Sdp back to normal
        sdp_subarray_proxy.SetDefective(False)

        # Invoke Abort() command on TMC
        tmc.invoke_abort()

        fixture["state"] = "Abort"
        assert subarray_obs_state_is_aborted()

        # Invoke Restart() command on TMC
        tmc.invoke_restart()

        fixture["state"] = "Restart"
        # Verify ObsState is EMPTY
        assert subarray_obs_state_is_empty()

        # Invoke AssignResources() Command on TMC
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")
        tmc.compose_sub(assign_json)
        LOGGER.info("AssignResources command is invoked successfully")

        # Verify ObsState is IDLE
        assert subarray_obs_state_is_idle()
        fixture["state"] ="AssignResources"

        # Invoke Configure() Command on TMC
        LOGGER.info("Invoking Configure command on TMC CentralNode")
        tmc.configure_subarray(config_json)

        # Verify ObsState is READY
        assert subarray_obs_state_is_ready()
        fixture["state"] = "Configure"

        # Invoke Scan() Command on TMC
        LOGGER.info("Invoking Scan command on TMC CentralNode")
        tmc.scan(scan_json)

        # Verify ObsState is READY
        assert subarray_obs_state_is_ready()
        fixture["state"] ="Scan"

        # Invoke End() Command on TMC
        LOGGER.info("Invoking End command on TMC SubarrayNode")
        tmc.end()

        # Verify ObsState is IDLE
        assert subarray_obs_state_is_idle()
        fixture["state"] = "End"

        # Invoke ReleaseResources() command on TMC
        tmc.invoke_releaseResources(release_json)

        fixture["state"] = "ReleaseResources"
        assert subarray_obs_state_is_empty()

        # Invoke TelescopeOff() command on TMC
        tmc.set_to_off()

        # Verify State transitions after TelescopeOff
        assert telescope_is_in_off_state()
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
