import pytest
from pytest_bdd import given, parsers, scenario, then, when

import tests.resources.test_support.tmc_helpers as tmc
from tests.conftest import LOGGER
from tests.resources.test_support.common_utils.tmc_helpers import TmcHelper
from tests.resources.test_support.constant import (
    DEVICE_OBS_STATE_EMPTY_INFO,
    DEVICE_OBS_STATE_IDLE_INFO,
    DEVICE_OBS_STATE_READY_INFO,
    DEVICE_STATE_OFF_INFO,
    DEVICE_STATE_ON_INFO,
    DEVICE_STATE_STANDBY_INFO,
    ON_OFF_DEVICE_COMMAND_DICT,
    centralnode,
    tmc_subarraynode1,
)
from tests.resources.test_support.mid.telescope_controls_mid import (
    TelescopeControlMid,
)

tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)
telescope_control = TelescopeControlMid()


@pytest.mark.SKA_mid
@scenario(
    "../features/successive_configure.feature",
    "TMC validates reconfigure functionality with different configuration",
)
def test_multiple_configure_functionality():
    """
    Test TMC allows multiple configuration

    """


@given("the TMC is On")
def given_tmc():
    tmc.check_devices()
    # Verify Telescope is Off/Standby
    assert telescope_control.is_in_valid_state(
        DEVICE_STATE_STANDBY_INFO, "State", wait_time=10
    )
    LOGGER.info("Staring up the Telescope")

    tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)
    LOGGER.info("TelescopeOn command is invoked successfully")

    assert telescope_control.is_in_valid_state(
        DEVICE_STATE_ON_INFO, "State", wait_time=10
    )

    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_EMPTY_INFO, "obsState", wait_time=10
    )


@given("the subarray is in IDLE obsState")
def given_subarray_in_idle(json_factory):
    assign_json = json_factory("multiple_assign1")
    # Invoke AssignResources() Command on TMC
    LOGGER.info("Invoking AssignResources command on TMC CentralNode")
    tmc_helper.compose_sub(assign_json, **ON_OFF_DEVICE_COMMAND_DICT)
    LOGGER.info("AssignResources command is invoked successfully")

    # Verify ObsState is IDLE
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_IDLE_INFO, "obsState", wait_time=10
    )


@when(parsers.parse("the command configure is issued with {input_json1}"))
def send_configure(json_factory, input_json1):
    configure_json1 = json_factory(input_json1)
    LOGGER.info("Invoking Configure command with configure_json1")
    # Invoke Configure() command
    tmc_helper.configure_subarray(
        configure_json1, **ON_OFF_DEVICE_COMMAND_DICT
    )
    LOGGER.info("Configure command is invoked successfully")


@then("the subarray transitions to obsState READY")
def check_for_ready():
    # Verify ObsState is READY
    LOGGER.info("Verifying obsState READY after first Configure")
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_READY_INFO, "obsState", wait_time=10
    )


@when(
    parsers.parse(
        "the next successive configure command is issued with {input_json2}"
    )
)
def send_next_configure(json_factory, input_json2):
    configure_json2 = json_factory(input_json2)
    LOGGER.info("Invoking Configure2 command with configure_json2")
    # Invoke successive Configure() command
    tmc_helper.reconfigure_subarray(
        configure_json2, **ON_OFF_DEVICE_COMMAND_DICT
    )
    LOGGER.info("Configure2 command is invoked successfully")
    LOGGER.info("Verifying obsState READY after Reconfigures")


@then("the subarray reconfigures changing its obsState to READY")
def check_for_reconfigure_ready():
    # Verify ObsState is READY
    LOGGER.info("Verifying obsState READY after Reconfigures")
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_READY_INFO, "obsState", wait_time=10
    )


@then("test goes for the tear down")
def tear_down(json_factory):
    release_json = json_factory("command_ReleaseResources")

    # Invoke End() command
    LOGGER.info("Invoking End command on TMC SubarrayNode")
    tmc_helper.end(**ON_OFF_DEVICE_COMMAND_DICT)

    # Verify ObsState is IDLE
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_IDLE_INFO, "obsState", wait_time=10
    )
    LOGGER.info("End command is invoked successfully")

    # Invoke ReleaseResources() command
    tmc_helper.invoke_releaseResources(
        release_json, **ON_OFF_DEVICE_COMMAND_DICT
    )

    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_EMPTY_INFO, "obsState", wait_time=10
    )

    # Invoke TelescopeOff() command
    tmc_helper.set_to_off(**ON_OFF_DEVICE_COMMAND_DICT)

    # Verify State transitions after TelescopeOff
    assert telescope_control.is_in_valid_state(
        DEVICE_STATE_OFF_INFO, "State", wait_time=10
    )
    LOGGER.info("Test completes.")
