import pytest
from tango import DeviceProxy

import tests.resources.test_support.tmc_helpers as tmc
from tests.conftest import LOGGER
from tests.resources.test_support.common_utils.result_code import ResultCode
from tests.resources.test_support.constant import (
    centralnode,
    tmc_subarraynode1,
)
from tests.resources.test_support.controls import (
    subarray_obs_state_is_empty,
    subarray_obs_state_is_idle,
    telescope_is_in_on_state,
    telescope_is_in_standby_state,
)
from tests.resources.test_support.helpers import resource
from tests.resources.test_support.sync_decorators import sync_assign_resources
from tests.resources.test_support.tmc_helpers import tear_down


@pytest.mark.SKA_mid
def test_assign_invalid_json(json_factory):
    try:
        # AssignResources and ReleaseResources is executed.
        assign_json = json_factory("command_invalid_assign_release")
        tmc.check_devices()

        # # Verify Telescope is Off/Standby
        assert telescope_is_in_standby_state()
        LOGGER.info("Staring up the Telescope")

        # # Invoke TelescopeOn() command on TMC
        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
        tmc.set_to_on()
        LOGGER.info("TelescopeOn command is invoked successfully")

        # # Verify State transitions after TelescopeOn
        assert telescope_is_in_on_state()

        # # Invoke AssignResources() Command on TMC
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")
        resource(tmc_subarraynode1).assert_attribute("State").equals("ON")
        resource(tmc_subarraynode1).assert_attribute("obsState").equals(
            "EMPTY"
        )
        central_node = DeviceProxy(centralnode)
        tmc.check_devices()
        ret_code, message = central_node.AssignResources(assign_json)

        # Assert with TaskStatus as REJECTED
        assert ret_code == 5
        LOGGER.info(message)

        # # Verify ObsState is EMPTY
        assert subarray_obs_state_is_empty()

        # # Invoke TelescopeStandby() command on TMC
        tmc.set_to_standby()

        # # Verify State transitions after TelescopeStandby
        assert telescope_is_in_standby_state()

        LOGGER.info("Tests complete.")
    except Exception:
        tear_down()


@pytest.mark.SKA_mid
def test_release_invalid_json(json_factory):
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")
    invalid_release_json = json_factory("command_invalid_assign_release")
    try:
        # # AssignResources and ReleaseResources is executed.
        tmc.check_devices()

        # # Verify Telescope is Off/Standby
        assert telescope_is_in_standby_state()
        LOGGER.info("Staring up the Telescope")

        # # Invoke TelescopeOn() command on TMC
        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
        tmc.set_to_on()
        LOGGER.info("TelescopeOn command is invoked successfully")

        # # Verify State transitions after TelescopeOn
        assert telescope_is_in_on_state()

        # # Invoke AssignResources() Command on TMC
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

        # # Verify ObsState is Idle
        assert subarray_obs_state_is_idle()

        # # Invoke ReleaseResources() command on TMC
        central_node = DeviceProxy(centralnode)
        ret_code, message = central_node.ReleaseResources(invalid_release_json)
        # Assert with TaskStatus as REJECTED
        assert ret_code == 5
        LOGGER.info(message)
        # Check if telescope is in previous state
        assert subarray_obs_state_is_idle()
        # Invoke release resources
        # # Invoke ReleaseResources() command on TMC
        tmc.invoke_releaseResources(release_json)

        assert subarray_obs_state_is_empty()

        # # Invoke TelescopeStandby() command on TMC
        tmc.set_to_standby()

        # # Verify State transitions after TelescopeStandby
        assert telescope_is_in_standby_state()

        LOGGER.info("Tests complete.")

    except Exception:
        tear_down(release_json)


@pytest.mark.SKA_mid
def test_invalid_receptor_ids(json_factory):
    """AssignResources and ReleaseResources is executed."""
    assign_json = json_factory("command_assign_resources_invalid_receptor_id")
    release_json = json_factory("command_ReleaseResources")
    tmc.check_devices()

    try:
        # Verify Telescope is Off/Standby
        assert telescope_is_in_standby_state()
        LOGGER.info("Staring up the Telescope")

        # # Invoke TelescopeOn() command on TMC
        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
        tmc.set_to_on()
        LOGGER.info("TelescopeOn command is invoked successfully")

        # # Verify State transitions after TelescopeOn
        assert telescope_is_in_on_state()

        # # Invoke AssignResources() Command on TMC
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")
        resource(tmc_subarraynode1).assert_attribute("State").equals("ON")
        resource(tmc_subarraynode1).assert_attribute("obsState").equals(
            "EMPTY"
        )
        try:
            central_node = DeviceProxy(centralnode)
            pytest.command_result = central_node.AssignResources(assign_json)
        except Exception as e:
            LOGGER.exception("The Exception is %s", e)
            tear_down(release_json)

        assert (
            "The following Receptor id(s) do not exist"
            in pytest.command_result[1][0]
        )
        assert pytest.command_result[0][0] == ResultCode.REJECTED

        # Invoke TelescopeStandby() command on TMC
        tmc.set_to_standby()

        # Verify State transitions after TelescopeOff
        assert telescope_is_in_standby_state()

    except Exception:
        LOGGER.info("Tearing down...")
        tear_down()
