"""Test case to validate negative scenario for
   Dish Vcc map configuration feature
"""
import pytest
from pytest_bdd import given, parsers, scenario, then, when
from tango import DevState

from tests.resources.test_harness.helpers import (
    prepare_json_args_for_centralnode_commands,
)
from tests.resources.test_support.common_utils.result_code import ResultCode


@pytest.mark.xfail(reason="fix in central node release 0.11.5")
@pytest.mark.SKA_mid
@scenario(
    "../features/load_dish_cfg_command_negative_scenario.feature",
    "TMC returns error message when non existent file is provided "
    "in configuration",
)
def test_central_node_return_error_for_invalid_file(
    central_node_mid, event_recorder, simulator_factory
):
    """This test validate that when non existent file
    provided in dish vcc configuration json then command is rejected
    with error
    Glossary:
    - "central_node_mid": fixture for a TMC CentralNode Mid under test
    which provides simulated master devices
    - "event_recorder": fixture for a MockTangoEventCallbackGroup
    for validating the subscribing and receiving events.
    - "simulator_factory": fixture for creating simulator devices for
    mid Telescope respectively.
    """


@pytest.mark.SKA_mid
@scenario(
    "../features/load_dish_cfg_command_negative_scenario.feature",
    "TMC returns error when invalid dish id is provided in configuration",
)
def test_central_node_return_error_for_invalid_dish_id():
    """This test validate that when invalid dish id provided
    in dish vcc map json then command is rejected with error
    """


@given("a TMC")
def given_tmc():
    """Given a TMC"""


@given("Telescope is in ON state")
def telescope_in_on_state(central_node_mid, event_recorder):
    """Move Telescope to ON state"""
    event_recorder.subscribe_event(
        central_node_mid.central_node, "telescopeState"
    )
    central_node_mid.move_to_on()
    assert event_recorder.has_change_event_occurred(
        central_node_mid.central_node,
        "telescopeState",
        DevState.ON,
    )


@when(
    parsers.parse(
        "I issue the command LoadDishCfg on TMC with non "
        "existent file {file_name} in configuration"
    )
)
def invoke_load_dish_cfg(central_node_mid, command_input_factory, file_name):
    """Call load_dish_cfg method which invoke LoadDishCfg
    command on CentralNode
    """
    # Prepare input for load dish configuration
    load_dish_cfg_json = prepare_json_args_for_centralnode_commands(
        f"load_dish_cfg_{file_name}", command_input_factory
    )

    result_code, message = central_node_mid.load_dish_vcc_configuration(
        load_dish_cfg_json
    )
    pytest.command_result_code = result_code
    pytest.command_result_message = message


@then(parsers.parse("TMC rejects the command with error {error_message}"))
def test_tmc_rejects_command_with_error(error_message):
    """Test validate that command failed with error message"""
    assert pytest.command_result_code == ResultCode.REJECTED
    assert error_message in pytest.command_result_message


@when(
    parsers.parse(
        "I issue the command LoadDishCfg on TMC with invalid {dish_id}"
    )
)
def invoke_command_with_invalid_dish_id(
    central_node_mid, command_input_factory, dish_id
):
    """Call load dish cfg command with invalid dish id"""
    # Prepare input for load dish configuration
    load_dish_cfg_json = prepare_json_args_for_centralnode_commands(
        "load_dish_cfg_invalid_dish_id", command_input_factory
    )

    result_code, message = central_node_mid.load_dish_vcc_configuration(
        load_dish_cfg_json
    )
    pytest.command_result_code = result_code
    pytest.command_result_message = message
