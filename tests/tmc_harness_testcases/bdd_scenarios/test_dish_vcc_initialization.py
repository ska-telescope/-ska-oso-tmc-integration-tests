"""
Test case to validate negative scenario for
   Dish Vcc map configuration feature
"""
import json

import pytest
from pytest_bdd import given, scenario, then, when

from tests.resources.test_harness.helpers import (
    wait_and_validate_device_attribute_value,
)
from tests.resources.test_support.common_utils.result_code import ResultCode


@pytest.mark.SKA_mid
@scenario(
    "../features/load_dish_cfg_initialization.feature",
    "TMC is able to load Dish-VCC configuration file during initialization "
    "of CSP Master Leaf Node",
)
def test_load_dish_vcc_after_initialization():
    """This test validate that TMC is able to load the dish vcc
    configuration after initialization
    """


@given("a TMC is using default version of dish vcc map")
def given_tmc_using_default_version(tmc_mid):
    """Given a TMC"""
    expected_source_dish_vcc_config = {
        "interface": "https://schema.skao.int/ska-mid-cbf-initsysparam/1.0",
        "tm_data_sources": [
            "car://gitlab.com/ska-telescope/ska-telmodel-data?main#tmdata"
        ],
        "tm_data_filepath": (
            "instrument/ska1_mid_itf/ska-mid-cbf-system-parameters.json"
        ),
    }
    assert (
        json.loads(tmc_mid.csp_master_leaf_node.sourceDishVccConfig)
        == expected_source_dish_vcc_config
    )


@when("I restart the CSP Master Leaf Node and Central Node is running")
def restart_csp_master_leaf_node(tmc_mid):
    """Restart Csp Master Leaf Node"""
    tmc_mid.RestartServer(server_type="CSP_MLN")

    assert wait_and_validate_device_attribute_value(
        tmc_mid.csp_master_leaf_node,
        "DishVccMapValidationResult",
        str(int(ResultCode.OK)),
    )


@then(
    "CSP Master Leaf Node should able to load dish vcc version "
    "set before restart"
)
def validate_csp_mln_dish_vcc_version(tmc_mid):
    """Validate CSP Master Leaf node report correct dish vcc version"""
    expected_source_dish_vcc_config = {
        "interface": "https://schema.skao.int/ska-mid-cbf-initsysparam/1.0",
        "tm_data_sources": [
            "car://gitlab.com/ska-telescope/ska-telmodel-data?main#tmdata"
        ],
        "tm_data_filepath": (
            "instrument/ska1_mid_itf/ska-mid-cbf-system-parameters.json"
        ),
    }
    assert (
        json.loads(tmc_mid.csp_master_leaf_node.sourceDishVccConfig)
        == expected_source_dish_vcc_config
    )


@then("TMC should report dish vcc config set to true")
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
