"""Test module for TMC-DISH On functionality"""

import json

import pytest
from pytest_bdd import given, scenario, then, when
from tango import DevState

from tests.resources.test_harness.helpers import (
    wait_and_validate_device_attribute_value,
)
from tests.resources.test_support.common_utils.result_code import ResultCode


@pytest.mark.SKA_mid1
@scenario(
    "../features/tmc_dish/dishln_kvalue_validation.feature",
    "TMC Validates and Reports K-Value set in Dish Leaf Nodes",
)
def test_tmc_validate_dln_kvalue_identical():
    """
    Test case to verify Dish-VCC validation functionality

    Glossary:
        - "central_node_mid": fixture for a TMC CentralNode under test
        which provides simulated master devices
        - "event_recorder": fixture for EventRecorder class
        - "tmc_mid": fixture to give TMC mid device server commands
    """


@given("a TMC with already loaded Dish-VCC map version")
def given_tmc_with_already_loaded_dish_vcc_config_version(central_node_mid):
    """Given a TMC with loaded Dish-VCC map version"""
    cspmln_validation_string = "TMC and CSP Master Dish Vcc Version is Same"
    central_node_dish_vcc_validation_status = {
        "dish": "ALL DISH OK",
        "ska_mid/tm_leaf_node/csp_master": cspmln_validation_string,
    }
    assert (
        json.loads(central_node_mid.central_node.DishVccValidationStatus)
        == central_node_dish_vcc_validation_status
    )
    assert central_node_mid.central_node.isDishVccConfigSet


@when("the Dish Leaf Node is restarted")
def restart_the_dish_leaf_nodes(tmc_mid):
    """Restart the dish leaf nodes"""
    # [0, 1, 2, 3] are index for dish leaf node list
    tmc_mid.RestartServer("DISHLN_0")
    tmc_mid.RestartServer("DISHLN_1")
    tmc_mid.RestartServer("DISHLN_2")
    tmc_mid.RestartServer("DISHLN_3")


@when(
    "the Dish Leaf Node verifies k-value set on Dish Leaf Node"
    + " and Dish Manager are identical"
)
def check_dishln_is_on_and_kvalue_validation_accomplished(central_node_mid):
    """Method to check dish leaf node are up and k-value
    validation is completed"""
    assert wait_and_validate_device_attribute_value(
        central_node_mid.dish_leaf_node_list[0], "State", DevState.ON
    )
    assert wait_and_validate_device_attribute_value(
        central_node_mid.dish_leaf_node_list[1], "State", DevState.ON
    )
    assert wait_and_validate_device_attribute_value(
        central_node_mid.dish_leaf_node_list[2], "State", DevState.ON
    )
    assert wait_and_validate_device_attribute_value(
        central_node_mid.dish_leaf_node_list[3], "State", DevState.ON
    )
    assert wait_and_validate_device_attribute_value(
        central_node_mid.dish_leaf_node_list[0],
        "kValueValidationResult",
        str(int(ResultCode.OK)),
    )
    assert wait_and_validate_device_attribute_value(
        central_node_mid.dish_leaf_node_list[1],
        "kValueValidationResult",
        str(int(ResultCode.OK)),
    )
    assert wait_and_validate_device_attribute_value(
        central_node_mid.dish_leaf_node_list[2],
        "kValueValidationResult",
        str(int(ResultCode.OK)),
    )
    assert wait_and_validate_device_attribute_value(
        central_node_mid.dish_leaf_node_list[3],
        "kValueValidationResult",
        str(int(ResultCode.OK)),
    )


@then("Dish Leaf Node reports it to the Central Node")
def check_kvalue_validation_result_event_received(
    central_node_mid, event_recorder
):
    """Method to check Central Node received the kValueValidation
    attribute event from respective dish leaf nodes.
    """
    for i in range(0, len(central_node_mid.dish_leaf_node_list)):
        event_recorder.subscribe_event(
            central_node_mid.dish_leaf_node_list[i], "kValueValidationResult"
        )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_leaf_node_list[0],
        "kValueValidationResult",
        str(int(ResultCode.OK)),
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_leaf_node_list[1],
        "kValueValidationResult",
        str(int(ResultCode.OK)),
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_leaf_node_list[2],
        "kValueValidationResult",
        str(int(ResultCode.OK)),
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_leaf_node_list[3],
        "kValueValidationResult",
        str(int(ResultCode.OK)),
    )


@then(
    "the Central Node continues with current operation as"
    + " their are no discrepancies"
)
def check_value_of_isdishvccconfigset_on_central_node(central_node_mid):
    """Method to verify isDishVccConfig attribute is true or
    false after dish leaf node report."""
    assert central_node_mid.central_node.isDishVccConfigSet
