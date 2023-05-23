import json

import pytest
from pytest_bdd import given, parsers, scenario, then, when
from tango import DeviceProxy

from tests.conftest import LOGGER
from tests.resources.test_support.common_utils.common_helpers import Waiter
from tests.resources.test_support.common_utils.result_code import ResultCode
from tests.resources.test_support.common_utils.tmc_helpers import (
    TmcHelper,
    tear_down,
)
from tests.resources.test_support.constant import (
    DEVICE_OBS_STATE_EMPTY_INFO,
    DEVICE_OBS_STATE_IDLE_INFO,
    DEVICE_OBS_STATE_READY_INFO,
    DEVICE_OBS_STATE_SCANNING_INFO,
    DEVICE_STATE_ON_INFO,
    DEVICE_STATE_STANDBY_INFO,
    ON_OFF_DEVICE_COMMAND_DICT,
    centralnode,
    tmc_subarraynode1,
)
from tests.resources.test_support.telescope_controls import (
    BaseTelescopeControl,
)

# noqa: E501
tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)
telescope_control = BaseTelescopeControl()


@pytest.mark.SKA_mid
@scenario(
    "../features/successful_scan_after_failed_configure.feature",
    "Successfully execute a scan after a failed attempt to configure",
)
def test_configure_resource_with_invalid_json():
    """
    Test Configure command with input as invalid json.

    """


@given(
    parsers.parse(
        "a subarray {subarray_id} with resources {resources_list} in obsState IDLE"  # noqa: E501
    )
)
def given_tmc(json_factory):
    release_json = json_factory("command_ReleaseResources")
    assign_json = json_factory("command_AssignResources")
    try:
        # Verify Telescope is Off/Standby
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )
        # Invoke TelescopeOn() command on TMC CentralNode
        tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)
        # Verify State transitions after TelescopeOn
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_ON_INFO, "State"
        )
        # Invoke AssignResources() Command on TMC
        tmc_helper.compose_sub(assign_json, **ON_OFF_DEVICE_COMMAND_DICT)

        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_IDLE_INFO, "obsState"
        )
    except Exception as e:
        LOGGER.exception("Exception occured %s" % e)
        LOGGER.info("In tear down")
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)


@when(
    parsers.parse(
        "I issue the command Configure passing an invalid JSON script to the subarray {subarray_id}"  # noqa: E501
    )
)
def send(
    json_factory,
):
    release_json = json_factory("command_ReleaseResources")
    try:
        configure_json = json_factory("command_Configure")
        release_json = json_factory("command_ReleaseResources")
        configure_json = json.loads(configure_json)
        del configure_json["csp"]["common"]["config_id"]
        subarray_node = DeviceProxy(tmc_subarraynode1)
        pytest.command_result = subarray_node.Configure(
            json.dumps(configure_json)
        )
    except Exception as e:
        LOGGER.exception("Exception occured %s" % e)
        LOGGER.info("In tear down")
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)


@then(parsers.parse("the subarray {subarray_id} returns an error message"))
def invalid_command_rejection():
    # asserting error message and result code received from subarray
    assert (
        "{'csp': {'common': {'config_id': ['Missing data for required field.']}}}"  # noqa: E501
        in pytest.command_result[1][0]
    )
    assert pytest.command_result[0][0] == ResultCode.REJECTED


@then(parsers.parse("the subarray {subarray_id} remains in obsState IDLE"))
def tmc_status():
    # Verify obsState transitions
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_IDLE_INFO, "obsState"
    )


@when("I issue the command Configure passing a correct JSON script")
def tmc_accepts_command_with_valid_json(json_factory):
    release_json = json_factory("command_ReleaseResources")
    try:
        configure_json = json_factory("command_Configure")
        # Invoke Configure() Command on TMC
        tmc_helper.configure_subarray(
            configure_json, **ON_OFF_DEVICE_COMMAND_DICT
        )
    except Exception as e:
        LOGGER.exception("Exception occured %s" % e)
        LOGGER.info("In tear down")
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)


@then("the subarray transitions to obsState READY")
def tmc_status_ready():
    the_waiter = Waiter()
    the_waiter.set_wait_for_specific_obsstate("READY", [tmc_subarraynode1])
    the_waiter.wait(100)
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_READY_INFO, "obsState"
    )


@when("I issue the command Scan")
def tmc_accepts_scan_command(json_factory):
    scan_json = json_factory("command_Scan")
    release_json = json_factory("command_ReleaseResources")
    try:
        subarray_node = DeviceProxy(tmc_subarraynode1)
        subarray_node.Scan(scan_json)
    except Exception as e:
        LOGGER.exception("Exception occured %s" % e)
        LOGGER.info("In tear down")
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)


@then("the subarray transitions to obsState SCANNING")
def tmc_status_scanning():
    the_waiter = Waiter()
    the_waiter.set_wait_for_specific_obsstate("SCANNING", [tmc_subarraynode1])
    the_waiter.wait(100)
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_SCANNING_INFO, "obsState"
    )


@when("I issue the command EndScan")
def tmc_accepts_endscan_command(json_factory):
    release_json = json_factory("command_ReleaseResources")
    try:
        tmc_helper.invoke_endscan(**ON_OFF_DEVICE_COMMAND_DICT)
    except Exception as e:
        LOGGER.exception("Exception occured %s" % e)
        LOGGER.info("In tear down")
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)


# @then("the subarray transitions to obsState READY")


@then("implements the teardown")
def teardown_the_tmc(json_factory):
    release_json = json_factory("command_ReleaseResources")
    tmc_helper.end(**ON_OFF_DEVICE_COMMAND_DICT)
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_IDLE_INFO, "obsState"
    )
    tmc_helper.invoke_releaseResources(
        release_json, **ON_OFF_DEVICE_COMMAND_DICT
    )
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
    )
    tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)
    assert telescope_control.is_in_valid_state(
        DEVICE_STATE_STANDBY_INFO, "State"
    )
