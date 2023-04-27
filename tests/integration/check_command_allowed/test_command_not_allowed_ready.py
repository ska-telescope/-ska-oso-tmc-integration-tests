import pytest
import tango
from pytest_bdd import given, parsers, scenario, then, when
from tango import DeviceProxy

from tests.conftest import LOGGER
from tests.resources.test_support.common_utils.tmc_helpers import (
    TmcHelper,
    tear_down,
)
from tests.resources.test_support.constant import (
    DEVICE_OBS_STATE_ABORT_INFO,
    DEVICE_OBS_STATE_EMPTY_INFO,
    DEVICE_OBS_STATE_IDLE_INFO,
    DEVICE_OBS_STATE_READY_INFO,
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


@pytest.mark.kk
@pytest.mark.SKA_mid
@scenario(
    "../features/check_command_not_allowed.feature",
    "Unexpected commands not allowed when TMC subarray is READY",
)
def test_command_not_valid_in_ready_obsState():
    """
    Test commands not allowed in SubarrayNode obsState.READY

    """


@given("the TMC is in ON state and the subarray is in READY obsState")
def given_tmc(json_factory):
    assign_json = json_factory("command_AssignResources")
    configure_json = json_factory("command_Configure")
    # Verify Telescope is Off/Standby
    assert telescope_control.is_in_valid_state(
        DEVICE_STATE_STANDBY_INFO, "State"
    )
    LOGGER.info("Staring up the Telescope")

    # Invoke TelescopeOn() command on TMC
    LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
    tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)
    LOGGER.info("TelescopeOn command is invoked successfully")

    # Verify State transitions after TelescopeOn
    assert telescope_control.is_in_valid_state(DEVICE_STATE_ON_INFO, "State")
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
    )

    # Invoke AssignResources() Command on TMC
    LOGGER.info("Invoking AssignResources command on TMC CentralNode")
    tmc_helper.compose_sub(assign_json, **ON_OFF_DEVICE_COMMAND_DICT)
    LOGGER.info("AssignResources command is invoked successfully")

    # Verify ObsState is IDLE
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_IDLE_INFO, "obsState"
    )

    # Invoke Configure() Command on TMC
    LOGGER.info("Invoking Configure command on TMC SubarrayNode")
    tmc_helper.configure_subarray(configure_json, **ON_OFF_DEVICE_COMMAND_DICT)
    LOGGER.info("Configure command is invoked successfully")

    # Verify ObsState is READY
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_READY_INFO, "obsState"
    )


@when(
    parsers.parse(
        "the command {unexpected_command} is invoked on that subarray"
    )
)
def send(json_factory, unexpected_command):
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")

    if unexpected_command == "AssignResources":
        with pytest.raises(Exception):
            LOGGER.info("Invoking AssignResources command on TMC CentralNode")
            tmc_helper.assign_resources(
                assign_json, **ON_OFF_DEVICE_COMMAND_DICT
            )
    elif unexpected_command == "ReleaseResources":
        with pytest.raises(Exception):
            LOGGER.info("Invoking ReleaseResources command on TMC CentralNode")
            tmc_helper.invoke_releaseResources(
                release_json, **ON_OFF_DEVICE_COMMAND_DICT
            )
    elif unexpected_command == "EndScan":
        with pytest.raises(Exception):
            LOGGER.info("Invoking EndScan command on TMC SubarrayNode")
            tmc_helper.invoke_endscan(**ON_OFF_DEVICE_COMMAND_DICT)
    # elif unexpected_command == "EndScan":
    #     with pytest.raises(Exception):
    #         LOGGER.info("Invoking EndScan command on TMC SubarrayNode")
    #         tmc_helper.invoke_endscan(**ON_OFF_DEVICE_COMMAND_DICT)
    else:
        LOGGER.info("Other invalid commands")


# TODO: Current version of TMC does not support ResultCode.REJECTED,
# once the implementation is introduced, below block will be updated.
@then(
    parsers.parse(
        "the TMC should reject the {unexpected_command} with ResultCode.Rejected"
    )
)
def invalid_command_rejection(unexpected_command):
    pass


@then("TMC subarray remains in READY obsState")
def tmc_status():
    # Verify SubarrayNode obsState
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_READY_INFO, "obsState"
    )


@then(
    parsers.parse("TMC executes the {permitted_command} command successfully")
)
def tmc_accepts_next_commands(json_factory, permitted_command):
    configure_json = json_factory("command_Configure")
    scan_file = json_factory("command_Scan")
    release_json = json_factory("command_ReleaseResources")
    # if permitted_command == "Configure":
    #     LOGGER.info(f"permitted command is: {permitted_command}")
    #     tmc_helper.configure_ready(configure_json, **ON_OFF_DEVICE_COMMAND_DICT)
    #     LOGGER.info("Invoking ReleaseResources command on TMC CentralNode")
    #     assert telescope_control.is_in_valid_state(DEVICE_OBS_STATE_READY_INFO, "obsState")
    #     tmc_helper.end(**ON_OFF_DEVICE_COMMAND_DICT)
    #     LOGGER.info("Invoking End command on TMC SubarrayNode")
    #     assert telescope_control.is_in_valid_state(DEVICE_OBS_STATE_IDLE_INFO, "obsState")
    #     tmc_helper.invoke_releaseResources(release_json,**ON_OFF_DEVICE_COMMAND_DICT)
    #     LOGGER.info("Invoking ReleaseResources command on TMC SubarrayNode")
    #     assert telescope_control.is_in_valid_state(DEVICE_STATE_ON_INFO, "State")
    #     assert telescope_control.is_in_valid_state(DEVICE_OBS_STATE_EMPTY_INFO, "obsState")
    #     tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)
    #     LOGGER.info("Invoking Standby command on TMC SubarrayNode")
    #     assert telescope_control.is_in_valid_state(DEVICE_STATE_STANDBY_INFO, "State")

    if permitted_command == "Scan":
        LOGGER.info(f"permitted command is: {permitted_command}")
        tmc_helper.scan(scan_file, **ON_OFF_DEVICE_COMMAND_DICT)
        LOGGER.info("Invoking Scan command on TMC SubarrayNode")
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_READY_INFO, "obsState"
        )
        tmc_helper.end(**ON_OFF_DEVICE_COMMAND_DICT)
        LOGGER.info("Invoking End command on TMC SubarrayNode")
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_IDLE_INFO, "obsState"
        )
        tmc_helper.invoke_releaseResources(
            release_json, **ON_OFF_DEVICE_COMMAND_DICT
        )
        LOGGER.info("Invoking ReleaseResources command on TMC SubarrayNode")
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_ON_INFO, "State"
        )
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
        )
        tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)
        LOGGER.info("Invoking Standby command on TMC SubarrayNode")
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )

    elif permitted_command == "End":
        tmc_helper.end(**ON_OFF_DEVICE_COMMAND_DICT)
        LOGGER.info("Invoking End command on TMC SubarrayNode")
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_IDLE_INFO, "obsState"
        )
        tmc_helper.invoke_releaseResources(
            release_json, **ON_OFF_DEVICE_COMMAND_DICT
        )
        LOGGER.info("Invoking ReleaseResources command on TMC SubarrayNode")
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_ON_INFO, "State"
        )
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
        )
        tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)
        LOGGER.info("Invoking Standby command on TMC SubarrayNode")
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )

    elif permitted_command == "Abort":
        tmc_helper.invoke_abort(**ON_OFF_DEVICE_COMMAND_DICT)
        LOGGER.info("Invoking Abort command on TMC SubarrayNode")
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_ABORT_INFO, "obsState"
        )
        tmc_helper.invoke_restart(**ON_OFF_DEVICE_COMMAND_DICT)
        LOGGER.info("Invoking Restart command on TMC SubarrayNode")
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_ON_INFO, "State"
        )
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
        )
        tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)
        LOGGER.info("Invoking Standby command on TMC SubarrayNode")
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )
    else:
        LOGGER.info(f"permitted command is: {permitted_command}")
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)
