import time
import pytest
import tango
from pytest_bdd import given, parsers, scenario, then, when
from tests.conftest import LOGGER
import tests.resources.test_support.tmc_helpers as tmc
from tests.resources.test_support.helpers import resource
from tests.resources.test_support.common_utils.common_helpers import resource
from tango import DeviceProxy
from tests.resources.test_support.constant import (
    tmc_subarraynode1,
    centralnode,
)
from tests.resources.test_support.common_utils.tmc_helpers import TmcHelper
from tests.resources.test_support.mid.telescope_controls_mid import TelescopeControlMid
from tests.resources.test_support.constant import (
    DEVICE_STATE_STANDBY_INFO,
    DEVICE_STATE_ON_INFO,
    DEVICE_OBS_STATE_EMPTY_INFO,
    ON_OFF_DEVICE_COMMAND_DICT,
    DEVICE_OBS_STATE_READY_INFO,
    ON_OFF_DEVICE_COMMAND_DICT,
)
from tests.resources.test_support.tmc_helpers import tear_down


tmc_helper=TmcHelper(centralnode, tmc_subarraynode1)
telescope_control = TelescopeControlMid()


@pytest.mark.SKA_mid
@scenario("../features/check_command_not_allowed.feature", "Unexpected commands not allowed when TMC busy in assigning the resources for a subarray")
def test_command_not_allowed():
    """Assigning the resources in RESOURCING obsState"""


@given("the TMC is in ON state and the subarray is busy in assigning the resources")
def given_tmc(json_factory):
    assign_json = json_factory("command_AssignResources")
    tmc.check_devices()
    assert telescope_control.is_in_valid_state(DEVICE_STATE_STANDBY_INFO, "State")
    LOGGER.info("Staring up the Telescope")
    tmc.set_to_on()
    assert telescope_control.is_in_valid_state(DEVICE_STATE_ON_INFO, "State")
    assert telescope_control.is_in_valid_state(DEVICE_OBS_STATE_EMPTY_INFO, "obsState")

    central_node = DeviceProxy(centralnode)
    tmc.check_devices()
    central_node.AssignResources(assign_json)
    LOGGER.info("Checking for Subarray node obsState")
    resource(tmc_subarraynode1).assert_attribute("obsState").equals("RESOURCING")
    LOGGER.info("Checking for Subarray node obsState")


@when(
    parsers.parse("the command {unexpected_command} is invoked on the subarray"))
def send_command(json_factory, unexpected_command):    
    if unexpected_command == "AssignResources":
        assign_json2 = json_factory("command_AssignResources_2")
        central_node = DeviceProxy(centralnode)
        central_node.command_inout(unexpected_command, assign_json2)
        LOGGER.info("Invoked AssignResources2 from CentralNode")
  

# TODO: Current version of TMC does not support ResultCode.REJECTED, 
# once the implementation is introduced, below block will be updated.
@then(parsers.parse("the TMC should reject the {unexpected_command} with ResultCode.Rejected"))
def invalid_command_rejection(unexpected_command):
    pass


@then(parsers.parse("TMC completes assigning the resources for that subarray, and executes the Configure command successfully"))
def tmc_accepts_permitted_commands(json_factory):
    configure_json = json_factory("command_Configure")
    release_json = json_factory("command_ReleaseResources")
    LOGGER.info("Invoking Configure command on TMC SubarrayNode")
    tmc_helper.configure_sub(configure_json,**ON_OFF_DEVICE_COMMAND_DICT)
    LOGGER.info("Configure command on TMC SubarrayNode is successful")
    assert telescope_control.is_in_valid_state(DEVICE_OBS_STATE_READY_INFO, "obsState")

    # tear down
    tmc_helper.invoke_releaseResources(release_json, **ON_OFF_DEVICE_COMMAND_DICT)
    LOGGER.info("ReleaseResources command on TMC SubarrayNode is successful")
    assert telescope_control.is_in_valid_state(DEVICE_OBS_STATE_EMPTY_INFO, "obsState")
    tmc_helper.set_to_off(**ON_OFF_DEVICE_COMMAND_DICT)
    LOGGER.info("ReleaseResources command on TMC SubarrayNode is successful")
    assert telescope_control.is_in_valid_state(DEVICE_STATE_STANDBY_INFO, "State")



