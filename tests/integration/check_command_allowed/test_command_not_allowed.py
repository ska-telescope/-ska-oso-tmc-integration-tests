import pytest
import tango
from pytest_bdd import given, parsers, scenario, then, when
from tests.resources.test_support.controls import telescope_is_in_standby_state, telescope_is_in_on_state, \
    telescope_is_in_off_state, subarray_obs_state_is_empty, subarray_obs_state_is_idle, subarray_obs_state_is_ready
from tests.resources.test_support.sync_decorators import sync_assign_resources, sync_configure, sync_end
from tests.resources.test_support.helpers import resource
from tango import DeviceProxy
from tests.resources.test_support.constant import (
    tmc_subarraynode1,
    centralnode
)
import tests.resources.test_support.tmc_helpers as tmc
from tests.conftest import LOGGER
from tests.resources.test_support.common_utils.common_file import send_commands

configure_resources_file = "command_Configure.json"
assign_resources_file = "command_AssignResources.json"


@pytest.mark.vm
@pytest.mark.SKA_mid
@scenario("../features/check_command_not_allowed.feature",
          "Invalid unexpected commands not allowed in the current stable obsState")
def test_command_not_valid_in_empty():
    """
    fucntion to check validation
    """


@given(parsers.parse("the TMC device/s state=On and obsState {initial_obsstate}"))
def given_tmc():
    """Verify Telescope is Off/Standby"""
    assert telescope_is_in_standby_state()
    LOGGER.info("Staring up the Telescope")

    """Invoke TelescopeOn() command on TMC"""
    LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
    tmc.set_to_on()
    LOGGER.info("TelescopeOn command is invoked successfully")

    """Verify State transitions after TelescopeOn"""
    assert telescope_is_in_on_state()
    assert subarray_obs_state_is_empty()


@when(
    parsers.parse("the command {unexpected_command} is invoked , throws an error"))
def send():
    send_commands()


@then(parsers.parse("the TMC device remains in state=On, and obsState {initial_obsstate}"))
def tmc_status():
    assert telescope_is_in_on_state()
    assert subarray_obs_state_is_empty()


@then(parsers.parse("TMC accepts correct/expected command {expected_command} and performs the operation"))
def tmc_accepts_next_commands():
    """Invoke AssignResources() Command on TMC"""
    LOGGER.info("Invoking AssignResources command on TMC CentralNode")

    @sync_assign_resources()
    def compose_sub():
        resource(tmc_subarraynode1).assert_attribute("State").equals(
            "ON"
        )
        resource(tmc_subarraynode1).assert_attribute("obsState").equals(
            "EMPTY"
        )
        assign_res_input = tmc.get_input_str(assign_resources_file)
        central_node = DeviceProxy(centralnode)
        central_node.AssignResources(assign_res_input)
        LOGGER.info("Invoked AssignResources on CentralNode")

    compose_sub()

    """Verify ObsState is Idle"""
    assert subarray_obs_state_is_idle()

    LOGGER.info("AssignResources command is invoked successfully")
