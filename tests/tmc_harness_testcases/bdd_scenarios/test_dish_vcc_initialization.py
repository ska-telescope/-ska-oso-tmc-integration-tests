"""
Test case to validate negative scenario for
   Dish Vcc map configuration feature
"""
import json

import pytest
from pytest_bdd import given, scenario, then, when

from tests.resources.test_harness.helpers import (
    device_attribute_changed,
    prepare_json_args_for_centralnode_commands,
    wait_and_validate_device_attribute_value,
)
from tests.resources.test_support.common_utils.result_code import ResultCode


@pytest.mark.test
@pytest.mark.SKA_mid
@scenario(
    "../features/load_dish_cfg_initialization.feature",
    "TMC is able to load Dish-VCC configuration file during initialization "
    "of CspMasterLeafNode",
)
def test_load_dish_vcc_after_initialization():
    """This test validate that TMC is able to load the dish vcc
    configuration after initialization
    """


@given("TMC with default version of dish vcc map")
def given_tmc_using_default_version(tmc_mid, command_input_factory):
    """Given a TMC"""
    expected_source_dish_vcc_config = (
        prepare_json_args_for_centralnode_commands(
            "default_load_dish_cfg", command_input_factory
        )
    )
    assert json.loads(
        tmc_mid.csp_master_leaf_node.sourceDishVccConfig
    ) == json.loads(expected_source_dish_vcc_config)


@when("I restart the CspMasterLeafNode and CentralNode is running")
def restart_csp_master_leaf_node(tmc_mid):
    """Restart Csp Master Leaf Node"""
    tmc_mid.RestartServer(server_type="CSP_MLN")

    assert wait_and_validate_device_attribute_value(
        tmc_mid.csp_master_leaf_node,
        "DishVccMapValidationResult",
        str(int(ResultCode.OK)),
    )


@then(
    "CSP Master Leaf Node should able to load Dish-VCC version "
    "set before restart"
)
def validate_csp_mln_dish_vcc_version(tmc_mid, command_input_factory):
    """Validate CSP Master Leaf node report correct dish vcc version"""
    expected_source_dish_vcc_config = (
        prepare_json_args_for_centralnode_commands(
            "default_load_dish_cfg", command_input_factory
        )
    )
    assert json.loads(
        tmc_mid.csp_master_leaf_node.sourceDishVccConfig
    ) == json.loads(expected_source_dish_vcc_config)


@then("TMC should report Dish-VCC config set to true")
def validate_central_node_dish_vcc_config(tmc_mid):
    """Validate Central Node report dish vcc config after restart"""
    assert tmc_mid.IsDishVccConfigSet
    # Validate Dish Vcc validation status
    result_string_to_match = {
        "ska_mid/tm_leaf_node/csp_master": "TMC and CSP Master Dish Vcc "
        "Version is Same",
        "dish": "ALL DISH OK",
    }
    assert (
        json.loads(tmc_mid.central_node.DishVccValidationStatus)
        == result_string_to_match
    )


@pytest.mark.SKA_mid
@scenario(
    "../features/load_dish_cfg_initialization.feature",
    "TMC is able to load Dish-VCC configuration file during initialization "
    "of CentralNode",
)
def test_load_dish_vcc_after_central_node_restart():
    """This test validate that TMC is able to load the dish vcc
    configuration after Central Node restart
    """


@when("I restart the CentralNode and CspMasterLeafNode is running")
def restart_central_node(tmc_mid):
    """Restart Csp Master Leaf Node"""
    tmc_mid.RestartServer(server_type="CENTRAL_NODE")


@then("TMC should set Dish-VCC config set to True after restart")
def validate_dish_vcc_config_flag(tmc_mid):
    """Validate Central Node report dish vcc config to true after restart"""
    assert wait_and_validate_device_attribute_value(
        tmc_mid.central_node.central_node,
        "IsDishVccConfigSet",
        True,
    )
    # Validate Dish Vcc validation status
    result_string_to_match = {
        "ska_mid/tm_leaf_node/csp_master": "TMC and CSP Master Dish Vcc "
        "Version is Same",
        "dish": "ALL DISH OK",
    }
    assert (
        json.loads(tmc_mid.central_node.DishVccValidationStatus)
        == result_string_to_match
    )


@pytest.mark.SKA_mid
@scenario(
    "../features/load_dish_cfg_initialization.feature",
    "TMC is able to load last used Dish-VCC configuration before restart",
)
def test_load_dish_vcc_after_restart():
    """This test validate that TMC is able to load the dish vcc
    map version which is set by calling LoadDishCfg command before restart
    """


@when(
    "I issue the command LoadDishCfg on TMC with Dish-VCC configuration file"
)
def invoke_load_dish_cfg_command(
    tmc_mid, event_recorder, command_input_factory
):
    """Invoke Load Dish Cfg"""
    # Subscribe for longRunningCommandResult attribute
    event_recorder.subscribe_event(
        tmc_mid.central_node.central_node, "longRunningCommandResult"
    )
    # Prepare input for load dish configuration
    load_dish_cfg_json = prepare_json_args_for_centralnode_commands(
        "load_dish_cfg", command_input_factory
    )

    _, unique_id = tmc_mid.load_dish_vcc_configuration(load_dish_cfg_json)

    assert event_recorder.has_change_event_occurred(
        tmc_mid.central_node.central_node,
        "longRunningCommandResult",
        (unique_id[0], str(int(ResultCode.OK))),
        lookahead=5,
    )


@then("TMC displays the current version of Dish-VCC configuration")
def validate_source_disc_vcc_param_attribute_set(
    tmc_mid, command_input_factory
):
    """Valdate sourceDishVccConfig and dishVccConfig attribute
    correctly set on csp master leaf node
    :param central_node_mid: fixture for a TMC CentralNode Mid under test
    which provides simulated master devices
    """
    expected_source_dish_vcc_config = (
        prepare_json_args_for_centralnode_commands(
            "load_dish_cfg", command_input_factory
        )
    )

    expected_dish_vcc_config = prepare_json_args_for_centralnode_commands(
        "load_dish_cfg_dish_vcc_map", command_input_factory
    )

    assert device_attribute_changed(
        device=tmc_mid.csp_master_leaf_node,
        attribute_name_list=["sourceDishVccConfig", "dishVccConfig"],
        attribute_value_list=[
            expected_source_dish_vcc_config,
            expected_dish_vcc_config,
        ],
        timeout=100,
    ), (
        "dishVccConfig and sourceDishVccConfig attribute value is not set "
        "on csp master leaf node"
    )


@when("I restart the CentralNode and CspMasterLeafNode")
def restart_central_node_and_csp_mln(tmc_mid):
    """Restart Csp Master Leaf Node"""
    tmc_mid.RestartServer(server_type="CSP_MLN")
    tmc_mid.RestartServer(server_type="CENTRAL_NODE")


@then("TMC should set version of Dish-VCC version used before restart")
def validate_dish_vcc_config_after_central_node_and_csp_mln_restart(
    tmc_mid, command_input_factory
):
    """Validate Central Node report dish vcc config to true after restart"""
    assert wait_and_validate_device_attribute_value(
        tmc_mid.central_node.central_node,
        "IsDishVccConfigSet",
        True,
    )
    # Validate Dish Vcc validation status
    result_string_to_match = {
        "ska_mid/tm_leaf_node/csp_master": "TMC and CSP Master Dish Vcc"
        " Version is Same",
        "dish": "ALL DISH OK",
    }
    assert (
        json.loads(tmc_mid.central_node.DishVccValidationStatus)
        == result_string_to_match
    )

    # Validate CSP Master Leaf Node report dish vcc config set before restart
    expected_source_dish_vcc_config = (
        prepare_json_args_for_centralnode_commands(
            "load_dish_cfg", command_input_factory
        )
    )

    expected_dish_vcc_config = prepare_json_args_for_centralnode_commands(
        "load_dish_cfg_dish_vcc_map", command_input_factory
    )

    assert json.loads(
        tmc_mid.csp_master_leaf_node.sourceDishVccConfig
    ) == json.loads(expected_source_dish_vcc_config)

    assert json.loads(
        tmc_mid.csp_master_leaf_node.dishVccConfig
    ) == json.loads(expected_dish_vcc_config)
