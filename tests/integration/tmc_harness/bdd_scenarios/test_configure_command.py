import pytest
from pytest_bdd import given, parsers, scenario, then, when

from tests.conftest import LOGGER
from tests.resources.test_support.common_utils.telescope_controls import (
    BaseTelescopeControl,
)
from tests.resources.test_support.common_utils.tmc_helpers import (
    TmcHelper,
    tear_down,
)
from tests.resources.test_support.constant_low import (
    DEVICE_OBS_STATE_EMPTY_INFO,
    DEVICE_OBS_STATE_IDLE_INFO,
    DEVICE_OBS_STATE_READY_INFO,
    DEVICE_STATE_ON_INFO,
    DEVICE_STATE_STANDBY_INFO,
    ON_OFF_DEVICE_COMMAND_DICT,
    centralnode,
    tmc_subarraynode1,
)

tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)
telescope_control = BaseTelescopeControl()


@pytest.mark.skip(
    reason="AssignResources and ReleaseResources"
    " functionalities are not yet"
    " implemented on mccs master leaf node."
)
@pytest.mark.SKA_low
@scenario(
    "../features/check_configure_command.feature",
    "TMC executes Configure commands",
)
def test_configure_command():
    """
    Test SubarrayNode Low Configure command.
    """


@given("the TMC is On")
def given_tmc(json_factory):
    release_json = json_factory("command_release_resource_low")
    try:
        # Verify Telescope is Off/Standby
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )

        # Invoke TelescopeOn() command on TMC CentralNode
        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
        tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify State transitions after TelescopeOn
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_ON_INFO, "State"
        )

    except Exception:
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)


@given("the subarray is in IDLE obsState")
def tmc_check_status(json_factory):
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
    )
    assign_json = json_factory("command_assign_resource_low")
    LOGGER.info("Invoking AssignResources command on TMC CentralNode")
    tmc_helper.compose_sub(assign_json, **ON_OFF_DEVICE_COMMAND_DICT)

    # Verify ObsState is IDLE
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_IDLE_INFO, "obsState"
    )


@when(
    parsers.parse("the command Configure is invoked with correct input_json")
)
def send(json_factory):
    release_json = json_factory("command_release_resource_low")
    try:
        configure_json = json_factory("command_Configure_low")
        LOGGER.info(f"Input argin for Configure: {configure_json}")

        # Invoke Configure() Command on TMC
        LOGGER.info("Invoking Configure command on TMC SubarrayNode")
        tmc_helper.configure_subarray(
            configure_json, **ON_OFF_DEVICE_COMMAND_DICT
        )
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_READY_INFO, "obsState"
        )

        # teardown
        LOGGER.info("Invoking END on TMC")
        tmc_helper.end(**ON_OFF_DEVICE_COMMAND_DICT)

        #  Verify obsState is IDLE
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_IDLE_INFO, "obsState"
        )

        LOGGER.info("Invoking ReleaseResources on TMC")
        tmc_helper.invoke_releaseResources(
            release_json, **ON_OFF_DEVICE_COMMAND_DICT
        )

        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
        )

        LOGGER.info("Invoking Telescope Standby on TMC")
        tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)

        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )
        LOGGER.info("Tear Down complete. Telescope is in Standby State")
    except Exception:
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)


@then("the subarray transitions to obsState READY")
def tmc_status():
    # Verify obsState transitions
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_READY_INFO, "obsState"
    )
