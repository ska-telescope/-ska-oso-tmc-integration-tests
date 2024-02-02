"""Test module for TMC-DISH On functionality"""

import json
import time

import pytest
from pytest_bdd import given, scenario, then, when
from tango import DeviceProxy, DevState

from tests.resources.test_harness.constant import tmc_csp_master_leaf_node
from tests.resources.test_harness.helpers import (
    wait_and_validate_device_attribute_value,
)
from tests.resources.test_harness.utils.enums import SimulatorDeviceType
from tests.resources.test_support.common_utils.result_code import ResultCode


@pytest.mark.SKA_mid
@scenario(
    "../features/tmc_dish/dishln_kvalue_validation.feature",
    "TMC Validates and Reports K-Value not set in Dish Leaf Nodes",
)
def test_tmc_validate_dln_kvalue_not_set():
    """
    Test case to verify Dish-VCC validation functionality

    Glossary:
        - "central_node_mid": fixture for a TMC CentralNode under test
        - "simulator_factory": fixture for SimulatorFactory class,
        which provides simulated master devices
        - "event_recorder": fixture for EventRecorder class
    """


@given("a TMC with already loaded Dish-VCC map version")
def given_tmc_with_already_loaded_dish_vcc_config_version(
    central_node_mid, simulator_factory
):
    """
    Given a TMC
    Check all the required devices are up and running
    Args:
        simulator_factory: fixture for SimulatorFactory class,
        which provides simulated master devices
    """
    csp_master_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.MID_CSP_MASTER_DEVICE
    )
    assert csp_master_sim.ping() > 0
    assert DeviceProxy(tmc_csp_master_leaf_node).ping() > 0
    assert central_node_mid.dish_master_list[0].ping() > 0
    assert central_node_mid.dish_master_list[1].ping() > 0
    assert central_node_mid.dish_master_list[2].ping() > 0
    assert central_node_mid.dish_master_list[3].ping() > 0
    assert central_node_mid.dish_leaf_node_list[0].ping() > 0
    assert central_node_mid.dish_leaf_node_list[1].ping() > 0
    assert central_node_mid.dish_leaf_node_list[2].ping() > 0
    assert central_node_mid.dish_leaf_node_list[3].ping() > 0
    assert central_node_mid.central_node.isDishVccConfigSet


@when("the Dish Leaf Node is restarted")
def restart_the_dish_leaf_nodes(central_node_mid, tmc_mid):
    """Restart the dish leaf nodes"""
    # Unset values on some of the Dish Leaf Nodes
    for i in range(0, 2):
        central_node_mid.dish_leaf_node_list[i].kValue = 0

    # Unset values on some of the Dish Managers
    for i in range(2, 4):
        central_node_mid.dish_master_list[i].kValue = 0

    # [0, 1, 2, 3] are index for dish leaf node list
    tmc_mid.RestartServer("DISHLN_0")
    tmc_mid.RestartServer("DISHLN_1")
    tmc_mid.RestartServer("DISHLN_2")
    tmc_mid.RestartServer("DISHLN_3")


@when(
    "the Dish Leaf Node finds k-value not set on either"
    + " of Dish Leaf Node or Dish Manager"
)
def check_dishln_is_on_and_kvalue_validation_accomplished(central_node_mid):
    """Method to check dish leaf node are up and
    k-value validation is completed"""
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
        str(int(ResultCode.UNKNOWN)),
    )
    assert wait_and_validate_device_attribute_value(
        central_node_mid.dish_leaf_node_list[1],
        "kValueValidationResult",
        str(int(ResultCode.UNKNOWN)),
    )
    assert wait_and_validate_device_attribute_value(
        central_node_mid.dish_leaf_node_list[2],
        "kValueValidationResult",
        str(int(ResultCode.UNKNOWN)),
    )
    assert wait_and_validate_device_attribute_value(
        central_node_mid.dish_leaf_node_list[3],
        "kValueValidationResult",
        str(int(ResultCode.UNKNOWN)),
    )


@then(
    "Dish Leaf Node reports k-value not set on either"
    + " of Dish Leaf Node or Dish Manager"
)
def check_kvalue_validadation_result_event_received(
    central_node_mid, event_recorder
):
    """Method to check Central Node received the kValueValidation
    attribute event from respective dish leaf nodes."""
    for i in range(0, 4):
        event_recorder.subscribe_event(
            central_node_mid.dish_leaf_node_list[i], "kValueValidationResult"
        )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_leaf_node_list[0],
        "kValueValidationResult",
        str(int(ResultCode.UNKNOWN)),
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_leaf_node_list[1],
        "kValueValidationResult",
        str(int(ResultCode.UNKNOWN)),
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_leaf_node_list[2],
        "kValueValidationResult",
        str(int(ResultCode.UNKNOWN)),
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_leaf_node_list[3],
        "kValueValidationResult",
        str(int(ResultCode.UNKNOWN)),
    )


@then(
    "the Central Node reports the same and prohibits "
    + "any further command execution"
)
def check_value_of_isdishvccconfigset_on_central_node(central_node_mid):
    """Method to verify isDishVccConfig attribute is true
    or false after dish leaf node report."""
    cspmln_validation_string = "TMC and CSP Master Dish Vcc Version is Same"
    central_node_dish_vcc_validation_status = {
        "d0001": "k-value not set",
        "d0036": "k-value not set",
        "d0063": "k-value not set",
        "d0100": "k-value not set",
        "ska_mid/tm_leaf_node/csp_master": cspmln_validation_string,
    }
    assert not central_node_mid.central_node.isDishVccConfigSet
    assert (
        json.loads(central_node_mid.central_node.DishVccValidationStatus)
        == central_node_dish_vcc_validation_status
    )
    # Central Node does not allow any command execution
    with pytest.raises(Exception) as e:
        central_node_mid.central_node.TelescopeOn()
    assert "Dish Vcc Config not Set" in str(e.value)
    # Restore to previous k-value
    central_node_mid.dish_leaf_node_list[0].SetKValue(111)
    central_node_mid.dish_leaf_node_list[1].SetKValue(222)
    central_node_mid.dish_leaf_node_list[2].SetKValue(333)
    central_node_mid.dish_leaf_node_list[3].SetKValue(444)

    assert wait_and_validate_device_attribute_value(
        central_node_mid.central_node,
        "isDishVccConfigSet",
        True,
    )
