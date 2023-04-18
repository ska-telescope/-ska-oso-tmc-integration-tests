import pytest
import tango
from pytest_bdd import given, parsers, scenario, then, when
from tests.conftest import LOGGER
from tests.resources.test_support.controls import telescope_is_in_standby_state, telescope_is_in_on_state, telescope_is_in_off_state, subarray_obs_state_is_empty, subarray_obs_state_is_idle
import tests.resources.test_support.tmc_helpers as tmc
from tests.resources.test_support.sync_decorators import sync_assign_resources
from tests.resources.test_support.helpers import resource, waiter
from tango import DeviceProxy
from tests.resources.test_support.constant import (
    tmc_subarraynode1,
    centralnode
)
from tests.resources.test_support.mid.telescope_controls_mid import TelescopeControlMid
from tests.resources.test_support.constant import (
    DEVICE_STATE_STANDBY_INFO,
    DEVICE_STATE_ON_INFO,
    DEVICE_OBS_STATE_EMPTY_INFO,
    ON_OFF_DEVICE_COMMAND_DICT,
)
from tests.resources.test_support.tmc_helpers import tear_down


@pytest.mark.hope
@scenario("../features/transional_obsstate_check_allowed.feature", "Invalid unexpected commands not allowed in the current transitional obsState")
def test_command_not_allowed():
    """Configure the Subarray in RESOURCING obsState"""


@given(parsers.parse(
    "the TMC device/s state=On and obsState {initial_obsstate}")
)
def given_tmc(json_factory):
    telescope_control = TelescopeControlMid()
    assign_json = json_factory("command_AssignResources")

    tmc.check_devices()

    # fixture = {}
    # fixture["state"] = "Unknown"

    assert telescope_control.is_in_valid_state(DEVICE_STATE_STANDBY_INFO, "State")
    LOGGER.info("Staring up the Telescope")
    tmc.set_to_on()
    assert telescope_control.is_in_valid_state(DEVICE_STATE_ON_INFO, "State")
    assert telescope_control.is_in_valid_state(DEVICE_OBS_STATE_EMPTY_INFO, "obsState")
    # tmc.compose_sub(assign_json,**ON_OFF_DEVICE_COMMAND_DICT)
    central_node = DeviceProxy(centralnode)
    tmc.check_devices()
    central_node.AssignResources(assign_json)
    LOGGER.info("Invoked AssignResources from CentralNode")
    LOGGER.info("Checking for SubarrayNode obsState")
    resource(tmc_subarraynode1).assert_attribute("obsState").equals("RESOURCING")


@when(
    parsers.parse("the command {unexpected_command} is invoked"))
def send_command(json_factory):
    assign_json = json_factory("command_AssignResources")
    central_node = DeviceProxy(centralnode)
    tmc.check_devices()
    central_node.AssignResources(assign_json)


@then("the command {unexpected_command} shows an error")
def command_responce():
    pass

@then(parsers.parse("the TMC device remains in state=On, and obsState {initial_obsstate}"))
def tmc_status():
   pass

@then(parsers.parse("TMC accepts correct/expected command {expected_command} and performs the operation"))
def tmc_accepts_next_commands():
    pass

