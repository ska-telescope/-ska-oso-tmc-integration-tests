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

tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)
telescope_control = BaseTelescopeControl()


@pytest.mark.SKA_mid
@scenario(
    "../features/successful_scan_after_failed_assigned.feature",
    "Successfully execute a scan after a failed attempt to assign resources",
)
def test_assign_resource_with_invalid_json():
    """
    Test AssignResource command with input as invalid json.

    """


@given(
    parsers.parse(
        "a subarray {subarray_id} with resources {resources_list} in obsState EMPTY"  # noqa: E501
    )
)
def given_tmc(json_factory):
    release_json = json_factory("command_ReleaseResources")
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
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
        )
    except Exception:
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)


@when(
    parsers.parse(
        "I issue the command AssignResources passing an invalid JSON script to the subarray {subarray_id}"  # noqa: E501
    )
)
def invoke_assign_resources_one(
    json_factory,
):
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")
    try:
        assign_json = json.loads(assign_json)
        del assign_json["sdp"]["processing_blocks"][0]["pb_id"]
        # Invoke AssignResources() Command on TMC
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")
        central_node = DeviceProxy(centralnode)
        pytest.command_result = central_node.AssignResources(
            json.dumps(assign_json)
        )
    except Exception as e:
        LOGGER.info("The Exception is %s", e)
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)


@then(parsers.parse("the subarray {subarray_id} returns an error message"))
def invalid_command_rejection():
    assert "JSON validation error" in pytest.command_result[1][0]
    assert pytest.command_result[0][0] == ResultCode.REJECTED


@then(parsers.parse("the subarray {subarray_id} remains in obsState EMPTY"))
def tmc_status():
    # Verify obsState transitions
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
    )


@when("I issue the command AssignResources passing a correct JSON script")
def tmc_accepts_command_with_valid_json(json_factory):
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")
    try:
        # Invoke AssignResources() Command on TMC
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")
        tmc_helper.compose_sub(assign_json, **ON_OFF_DEVICE_COMMAND_DICT)
    except Exception as e:
        LOGGER.info("The Exception is %s", e)
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)


@then("the subarray transitions to obsState IDLE")
def tmc_status_idle(json_factory):
    # Verify obsState is IDLE
    assert telescope_control.is_in_valid_state(
        DEVICE_OBS_STATE_IDLE_INFO, "obsState"
    )


@when("I issue the command Configure passing a correct JSON script")
def tmc_accepts_configure_command_with_valid_json(json_factory):
    configure_json = json_factory("command_Configure")
    release_json = json_factory("command_ReleaseResources")
    try:
        tmc_helper.configure_subarray(
            configure_json, **ON_OFF_DEVICE_COMMAND_DICT
        )
        LOGGER.info("Invoked Configure command on TMC SubarrayNode")
    except Exception:
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)


@then("the subarray transitions to obsState READY")
def tmc_status_ready():
    the_waiter = Waiter()
    the_waiter.set_wait_for_specific_obsstate("READY", [tmc_subarraynode1])
    the_waiter.wait(100)
    # Verify that the obstate is READY
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
        LOGGER.info("Invoked Scan command on TMC Subarray Node")
    except Exception as e:
        LOGGER.info("The Exception is %s", e)
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)


@then("the subarray transitions to obsState SCANNING")
def tmc_status_scanning(json_factory):
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
        subarray_node = DeviceProxy(tmc_subarraynode1)
        subarray_node.EndScan()
        LOGGER.info("Invoking EndScan command on TMC SubarrayNode")
        the_waiter = Waiter()
        the_waiter.set_wait_for_specific_obsstate("READY", [tmc_subarraynode1])
        the_waiter.wait(100)
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_READY_INFO, "obsState"
        )

    except Exception:
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)
        LOGGER.info("Tear Down complete. Telescope is in Standby State")


# @then("the subarray transitions to obsState READY")


@then("implements the teardown")
def teardown_the_tmc(json_factory):
    release_json = json_factory("command_ReleaseResources")
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
        DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
    )
    tmc_helper.set_to_standby(**ON_OFF_DEVICE_COMMAND_DICT)
    LOGGER.info("Invoking Standby command on TMC SubarrayNode")
    assert telescope_control.is_in_valid_state(
        DEVICE_STATE_STANDBY_INFO, "State"
    )


@pytest.mark.SKA_mid
@scenario(
    "../features/successful_scan_after_failed_assigned.feature",
    "Successfully execute a scan after a successive failed attempt to assign resources",  # noqa: E501
)
def test_assign_resource_after_successive_assign_failure():
    """
    Test successful Scan after after invoking AssignResource command with
    different invalid json.

    """


@when(
    parsers.parse(
        "I issue the command AssignResources passing an invalid JSON script2 to the subarray {subarray_id}"  # noqa: E501
    )
)
def send_assignresource_with_invalid_json2(
    json_factory,
):
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")
    try:
        assign_json = json.loads(assign_json)
        del assign_json["sdp"]["execution_block"]["scan_types"][0][
            "scan_type_id"
        ]
        # Invoke AssignResources() Command on TMC
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")
        central_node = DeviceProxy(centralnode)
        pytest.command_result = central_node.AssignResources(
            json.dumps(assign_json)
        )
    except Exception as e:
        LOGGER.info("The Exception is %s", e)
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)


@when(
    parsers.parse(
        "I issue the command AssignResources passing an invalid JSON script3 to the subarray {subarray_id}"  # noqa: E501
    )
)
def send_assignresource_with_invalid_json3(
    json_factory,
):
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")
    try:
        assign_json = json.loads(assign_json)
        del assign_json["sdp"]["execution_block"]["channels"][0]["channels_id"]
        # Invoke AssignResources() Command on TMC
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")
        central_node = DeviceProxy(centralnode)
        pytest.command_result = central_node.AssignResources(
            json.dumps(assign_json)
        )
    except Exception as e:
        LOGGER.info("The Exception is %s", e)
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)


@pytest.mark.kk
@pytest.mark.SKA_mid
@scenario(
    "../features/successful_scan_after_assigning_unavailable_resources.feature",  # noqa: E501
    "Successfully execute a scan after invoking assign resources with unavailable resources",  # noqa: E501
)
def test_assign_resource_with_unavailable_resources():
    """
    Test successful Scan after invoking AssignResource command with
    unavailable resources.

    """


@when(
    parsers.parse(
        "I issue the command AssignResources with unavailable resources {resources_list} to the subarray {subarray_id}"  # noqa: E501
    )
)
def invoke_assign_resources_two(json_factory, resources_list):
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")
    try:
        assign_json = json.loads(assign_json)
        assign_json["dish"]["receptor_ids"][0] = resources_list
        # Invoke AssignResources() Command on TMC
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")
        central_node = DeviceProxy(centralnode)
        pytest.command_result = central_node.AssignResources(
            json.dumps(assign_json)
        )
    except Exception as e:
        LOGGER.info("The Exception is %s", e)
        tear_down(release_json, **ON_OFF_DEVICE_COMMAND_DICT)


@then(
    parsers.parse(
        "the subarray {subarray_id} returns an error message with {resorces_list}"  # noqa: E501
    )
)  # noqa: E501
def invalid_command_rejection_with_unavailable_resources(resources_list):
    assert (
        "The following Receptor id(s) do not exist:"
    ) and resources_list in pytest.command_result[1][0]
    assert pytest.command_result[0][0] == ResultCode.REJECTED


@pytest.mark.SKA_mid
@scenario(
    "../features/successful_scan_after_assigning_unavailable_resources.feature",  # noqa: E501
    "Successfully execute a scan after invoking successive assign resources with unavailable resources",  # noqa: E501
)
def test_assign_resource_successive_invokation_with_unavailable_resources():
    """
    Test successful execution of Scan after successful invokation of
    AssignResource command with unavailable resources.
    """


@pytest.mark.SKA_mid
@scenario(
    "../features/successful_scan_after_combination_of_failed_assign_resources.feature",  # noqa: E501
    "Successfully execute a scan after combination of failed assign resources",  # noqa: E501
)
def test_assign_resource_with_combination():
    """
    Test successful Scan after invoking AssignResource with combination of
    invalid json and unavailable resources.
    Sequence
    1. Unavailable Resources
    2. Invalid json
    """


@pytest.mark.SKA_mid
@scenario(
    "../features/successful_scan_after_combination_of_failed_assign_resources.feature",  # noqa: E501
    "Successfully execute a scan after second combination of failed assign resources",  # noqa: E501
)
def test_assign_resource_with_second_combination():
    """
    Test successful Scan after invoking AssignResource command with
    combination of invalid json and unavailable resources.
    Sequence:
    1. Invalid json
    2. Unavailable Resources
    """
