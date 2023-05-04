import json
import time

import pytest
from tango import DeviceProxy

import tests.resources.test_support.tmc_helpers as tmc
from tests.conftest import LOGGER
from tests.resources.test_support.constant import (
    centralnode,
    csp_subarray1,
    dish_master1,
    tmc_subarraynode1,
)
from tests.resources.test_support.controls import (
    subarray_obs_state_is_aborted,
    subarray_obs_state_is_empty,
    subarray_obs_state_is_idle,
    subarray_obs_state_is_ready,
    telescope_is_in_on_state,
    telescope_is_in_standby_state,
)
from tests.resources.test_support.helpers import resource, waiter
from tests.resources.test_support.tmc_helpers import tear_down


@pytest.mark.SKA_mid
def test_abort_restart(json_factory):
    """Abort and Restart is executed."""
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
        tmc.compose_sub(assign_json)
        LOGGER.info("AssignResources command is invoked successfully")

        # Verify ObsState is IDLE
        assert subarray_obs_state_is_idle()

        # Invoke Abort() command on TMC
        LOGGER.info("Invoking Abort command on TMC")
        tmc.invoke_abort()
        LOGGER.info("Abort command is invoked successfully")

        assert subarray_obs_state_is_aborted()

        # Invoke Restart() command on TMC
        tmc.invoke_restart()

        # Verify ObsState is EMPTY
        assert subarray_obs_state_is_empty()

        # Invoke TelescopeStandby() command on TMC
        tmc.set_to_standby()

        # Verify State transitions after TelescopeStandby
        assert telescope_is_in_standby_state()

        LOGGER.info("Tests complete.")

    except Exception:
        tear_down(release_json)


@pytest.mark.SKA_mid
def test_abort_in_empty():
    """Abort and Restart is executed."""
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

        # Verify ObsState is EMPTY
        assert subarray_obs_state_is_empty()

        # Invoke Abort() command on TMC
        with pytest.raises(Exception):
            tmc.invoke_abort()

        # Invoke TelescopeStandby() command on TMC
        tmc.set_to_standby()

        # Verify State transitions after TelescopeStandby
        assert telescope_is_in_standby_state()

        LOGGER.info("Tests complete.")

    except Exception:
        tear_down()


@pytest.mark.SKA_mid
def test_abort_in_resourcing(json_factory):
    """Abort and Restart is executed."""
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")
    config_json = json_factory("command_Configure")
    scan_json = json_factory("command_Scan")
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

        # Setting CSP subarray as defective
        csp_subarray_proxy = DeviceProxy(csp_subarray1)
        csp_subarray_proxy.SetDefective(True)

        # Invoke AssignResources() Command on TMC
        resource(tmc_subarraynode1).assert_attribute("State").equals("ON")
        resource(tmc_subarraynode1).assert_attribute("obsState").equals(
            "EMPTY"
        )
        central_node = DeviceProxy(centralnode)
        central_node.AssignResources(assign_json)
        LOGGER.info("Invoked AssignResources on CentralNode")

        # Verify ObsState is RESOURCING
        the_waiter = waiter()
        the_waiter.set_wait_for_intermediate_obsstate(
            "RESOURCING", [tmc_subarraynode1]
        )
        the_waiter.wait(20)

        # Setting CSP back to normal
        csp_subarray_proxy.SetDefective(False)
        time.sleep(0.1)

        # Invoke Abort() command on TMC
        LOGGER.info("Invoking Abort command on TMC")
        tmc.invoke_abort()
        LOGGER.info("Abort command is invoked successfully")

        assert subarray_obs_state_is_aborted()

        # Invoke Restart() command on TMC
        tmc.invoke_restart()

        # Verify ObsState is EMPTY
        assert subarray_obs_state_is_empty()

        # Invoke AssignResources() Command on TMC
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")
        tmc.compose_sub(assign_json)
        LOGGER.info("AssignResources command is invoked successfully")

        # Verify ObsState is IDLE
        assert subarray_obs_state_is_idle()

        # Invoke Configure() Command on TMC
        LOGGER.info("Invoking Configure command on TMC CentralNode")
        tmc.configure_subarray(config_json)

        # Verify ObsState is READY
        assert subarray_obs_state_is_ready()

        # Invoke Scan() Command on TMC
        LOGGER.info("Invoking Scan command on TMC CentralNode")
        tmc.scan(scan_json)

        # Verify ObsState is READY
        assert subarray_obs_state_is_ready()

        # Invoke End() Command on TMC
        LOGGER.info("Invoking End command on TMC SubarrayNode")
        tmc.end()

        # Verify ObsState is IDLE
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


@pytest.mark.SKA_mid
def test_abort_in_resourcing_different_resources(json_factory):
    """Abort and Restart is executed."""
    assign_json = json_factory("command_AssignResources")
    assign_json2 = json_factory("command_AssignResources_2")
    release_json = json_factory("command_ReleaseResources")
    config_json = json_factory("command_Configure_2")
    scan_json = json_factory("command_Scan")

    # Modify release json
    release_json = json.loads(release_json)
    release_json["transaction_id"] = "txn-local-20210203-0002"
    release_json = json.dumps(release_json)

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

        # Setting CSP subarray as defective
        csp_subarray_proxy = DeviceProxy(csp_subarray1)
        csp_subarray_proxy.SetDefective(True)

        # Invoke AssignResources() Command on TMC
        resource(tmc_subarraynode1).assert_attribute("State").equals("ON")
        resource(tmc_subarraynode1).assert_attribute("obsState").equals(
            "EMPTY"
        )
        central_node = DeviceProxy(centralnode)
        central_node.AssignResources(assign_json)
        LOGGER.info("Invoked AssignResources on CentralNode")

        # Verify ObsState is RESOURCING
        the_waiter = waiter()
        the_waiter.set_wait_for_intermediate_obsstate(
            "RESOURCING", [tmc_subarraynode1]
        )
        the_waiter.wait(20)

        # Setting CSP back to normal
        csp_subarray_proxy.SetDefective(False)
        time.sleep(0.1)

        # Invoke Abort() command on TMC
        LOGGER.info("Invoking Abort command on TMC")
        tmc.invoke_abort()
        LOGGER.info("Abort command is invoked successfully")

        assert subarray_obs_state_is_aborted()

        # Invoke Restart() command on TMC
        tmc.invoke_restart()

        # Verify ObsState is EMPTY
        assert subarray_obs_state_is_empty()

        # Invoke AssignResources() Command on TMC
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")
        tmc.compose_sub(assign_json2)
        LOGGER.info("AssignResources command is invoked successfully")

        # Verify ObsState is IDLE
        assert subarray_obs_state_is_idle()

        # Invoke Configure() Command on TMC
        LOGGER.info("Invoking Configure command on TMC CentralNode")
        tmc.configure_subarray(config_json)

        # Verify ObsState is READY
        assert subarray_obs_state_is_ready()

        # Invoke Scan() Command on TMC
        LOGGER.info("Invoking Scan command on TMC CentralNode")
        tmc.scan(scan_json)

        # Verify ObsState is READY
        assert subarray_obs_state_is_ready()

        # Invoke End() Command on TMC
        LOGGER.info("Invoking End command on TMC SubarrayNode")
        tmc.end()

        # Verify ObsState is IDLE
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


@pytest.mark.SKA_mid
def test_abort_in_resourcing_with_second_abort(json_factory):
    """Abort and Restart is executed."""
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")
    config_json = json_factory("command_Configure")
    scan_json = json_factory("command_Scan")
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

        # Setting CSP subarray as defective
        csp_subarray_proxy = DeviceProxy(csp_subarray1)
        csp_subarray_proxy.SetDefective(True)

        # Invoke AssignResources() Command on TMC
        resource(tmc_subarraynode1).assert_attribute("State").equals("ON")
        resource(tmc_subarraynode1).assert_attribute("obsState").equals(
            "EMPTY"
        )
        central_node = DeviceProxy(centralnode)
        central_node.AssignResources(assign_json)
        LOGGER.info("Invoked AssignResources on CentralNode")

        # Verify ObsState is RESOURCING
        the_waiter = waiter()
        the_waiter.set_wait_for_intermediate_obsstate(
            "RESOURCING", [tmc_subarraynode1]
        )
        the_waiter.wait(20)

        # Setting SDP and CSP back to normal
        csp_subarray_proxy.SetDefective(False)
        time.sleep(0.1)

        # Invoke Abort() command on TMC
        subarray_node = DeviceProxy(tmc_subarraynode1)
        subarray_node.Abort()
        LOGGER.info("Invoked Abort on SubarrayNode")

        # Invoke Abort() command on TMC
        with pytest.raises(Exception):
            tmc.invoke_abort()

        time.sleep(1)

        assert subarray_obs_state_is_aborted()

        # Invoke Restart() command on TMC
        tmc.invoke_restart()

        # Verify ObsState is EMPTY
        assert subarray_obs_state_is_empty()

        # Invoke AssignResources() Command on TMC
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")
        tmc.compose_sub(assign_json)
        LOGGER.info("AssignResources command is invoked successfully")

        # Verify ObsState is IDLE
        assert subarray_obs_state_is_idle()

        # Invoke Configure() Command on TMC
        LOGGER.info("Invoking Configure command on TMC CentralNode")
        tmc.configure_subarray(config_json)

        # Verify ObsState is READY
        assert subarray_obs_state_is_ready()

        # Invoke Scan() Command on TMC
        LOGGER.info("Invoking Scan command on TMC CentralNode")
        tmc.scan(scan_json)

        # Verify ObsState is READY
        assert subarray_obs_state_is_ready()

        # Invoke End() Command on TMC
        LOGGER.info("Invoking End command on TMC SubarrayNode")
        tmc.end()

        # Verify ObsState is IDLE
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


@pytest.mark.SKA_mid
def test_abort_in_configuring(json_factory):
    """Abort and Restart is executed."""
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")
    config_json = json_factory("command_Configure")
    scan_json = json_factory("command_Scan")
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
        tmc.compose_sub(assign_json)

        # Verify ObsState is IDLE
        assert subarray_obs_state_is_idle()

        # Setting CSP subarray as defective
        csp_subarray_proxy = DeviceProxy(csp_subarray1)
        csp_subarray_proxy.SetDefective(True)

        # Invoke Configure() Command on TMC
        LOGGER.info("Invoking Configure command on TMC CentralNode")
        resource(tmc_subarraynode1).assert_attribute("obsState").equals("IDLE")
        subarray_node = DeviceProxy(tmc_subarraynode1)
        subarray_node.Configure(config_json)
        LOGGER.info("Invoked Configure on SubarrayNode")

        # Verify ObsState is CONFIGURING
        the_waiter = waiter()
        the_waiter.set_wait_for_intermediate_obsstate(
            "CONFIGURING", [tmc_subarraynode1, csp_subarray1]
        )
        the_waiter.wait(20)

        # Setting CSP back to normal
        csp_subarray_proxy.SetDefective(False)
        time.sleep(0.5)

        resource(csp_subarray1).assert_attribute("defective").equals(False)

        # Invoke Abort() command on TMC
        LOGGER.info("Invoking Abort command on TMC")
        tmc.invoke_abort()
        LOGGER.info("Abort command is invoked successfully")

        assert subarray_obs_state_is_aborted()

        dish_master = DeviceProxy(dish_master1)
        assert dish_master.pointingState == 1

        # Invoke Restart() command on TMC
        tmc.invoke_restart()

        # Verify ObsState is EMPTY
        assert subarray_obs_state_is_empty()

        # Invoke AssignResources() Command on TMC
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")
        tmc.compose_sub(assign_json)
        LOGGER.info("AssignResources command is invoked successfully")

        # Verify ObsState is IDLE
        assert subarray_obs_state_is_idle()

        # Invoke Configure() Command on TMC
        LOGGER.info("Invoking Configure command on TMC CentralNode")
        tmc.configure_subarray(config_json)

        # Verify ObsState is READY
        assert subarray_obs_state_is_ready()

        # Invoke Scan() Command on TMC
        LOGGER.info("Invoking Scan command on TMC CentralNode")
        tmc.scan(scan_json)

        # Verify ObsState is READY
        assert subarray_obs_state_is_ready()

        # Invoke End() Command on TMC
        LOGGER.info("Invoking End command on TMC SubarrayNode")
        tmc.end()

        # Verify ObsState is IDLE
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


@pytest.mark.SKA_mid
def test_abort_in_scanning(json_factory):
    """Abort and Restart is executed."""
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")
    config_json = json_factory("command_Configure")
    scan_json = json_factory("command_Scan")
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
        tmc.compose_sub(assign_json)

        # Verify ObsState is IDLE
        assert subarray_obs_state_is_idle()

        # Invoke Configure() Command on TMC
        LOGGER.info("Invoking Configure command on TMC CentralNode")
        tmc.configure_subarray(config_json)

        # Verify ObsState is READY
        assert subarray_obs_state_is_ready()

        # Setting CSP subarray as defective
        csp_subarray_proxy = DeviceProxy(csp_subarray1)
        csp_subarray_proxy.SetDefective(True)

        # Invoke Scan() Command on TMC
        resource(tmc_subarraynode1).assert_attribute("obsState").equals(
            "READY"
        )
        subarray_node = DeviceProxy(tmc_subarraynode1)
        subarray_node.Scan(scan_json)
        LOGGER.info("Invoked Scan on SubarrayNode")

        time.sleep(1)

        # Verify ObsState is SCANNING
        the_waiter = waiter()
        the_waiter.set_wait_for_intermediate_obsstate(
            "SCANNING", [tmc_subarraynode1]
        )
        the_waiter.wait(20)

        # Setting CSP back to normal
        csp_subarray_proxy.SetDefective(False)
        time.sleep(0.5)

        # Invoke Abort() command on TMC
        LOGGER.info("Invoking Abort command on TMC")
        tmc.invoke_abort()
        LOGGER.info("Abort command is invoked successfully")

        assert subarray_obs_state_is_aborted()

        # Invoke Restart() command on TMC
        tmc.invoke_restart()

        # Verify ObsState is EMPTY
        assert subarray_obs_state_is_empty()

        # Invoke AssignResources() Command on TMC
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")
        tmc.compose_sub(assign_json)
        LOGGER.info("AssignResources command is invoked successfully")

        # Verify ObsState is IDLE
        assert subarray_obs_state_is_idle()

        # Invoke Configure() Command on TMC
        LOGGER.info("Invoking Configure command on TMC CentralNode")
        tmc.configure_subarray(config_json)

        # Verify ObsState is READY
        assert subarray_obs_state_is_ready()

        # Invoke Scan() Command on TMC
        LOGGER.info("Invoking Scan command on TMC CentralNode")
        tmc.scan(scan_json)

        # Verify ObsState is READY
        assert subarray_obs_state_is_ready()

        # Invoke End() Command on TMC
        LOGGER.info("Invoking End command on TMC SubarrayNode")
        tmc.end()

        # Verify ObsState is IDLE
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
