import time
import pytest
import tango
from pytest_bdd import given, parsers, scenario, then, when
from tests.conftest import LOGGER
from tests.resources.test_support.controls import telescope_is_in_standby_state, telescope_is_in_on_state, telescope_is_in_off_state, subarray_obs_state_is_empty, subarray_obs_state_is_idle
import tests.resources.test_support.tmc_helpers as tmc
from tests.resources.test_support.sync_decorators import sync_assign_resources
from tests.resources.test_support.helpers import resource, waiter
from tests.resources.test_support.common_utils.common_helpers import Waiter, resource
from tango import DeviceProxy
from tests.resources.test_support.constant import (
    tmc_subarraynode1,
    centralnode, csp_subarray1, sdp_subarray1,
)
from tests.resources.test_support.common_utils.tmc_helpers import TmcHelper
from tests.resources.test_support.common_utils.sync_decorators import sync_configure, wait_assign
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


@pytest.mark.SKA_mid
@scenario("../features/transional_obsstate_check_allowed.feature", "Invalid unexpected commands not allowed in the current transitional obsState")
def test_command_not_allowed():
    """Assigning the resources in RESOURCING obsState"""


@given(parsers.parse(
    "the TMC device/s state=On and obsState {initial_obsstate}")
)
def given_tmc(json_factory):
    telescope_control = TelescopeControlMid()
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

    # time.sleep(1)
    resource(tmc_subarraynode1).assert_attribute("obsState").equals("RESOURCING")
    # tmc_helper.compose_sub(assign_json, **ON_OFF_DEVICE_COMMAND_DICT)
    LOGGER.info("Checking for Subarray node obsState")


@when(
    parsers.parse("the command {unexpected_command} is invoked, it shows an error"))
def send_command(json_factory, unexpected_command):
    try:
        assign_json2 = json_factory("command_AssignResources_2")
        central_node = DeviceProxy(centralnode)
        pytest.command_result = central_node.command_inout(unexpected_command, assign_json2)
        LOGGER.info("Invoked AssignResources2 from CentralNode")
    except Exception as ex:
        assert "StateModelError" in str(ex)
        pytest.command_result = "StateModelError"
    # try:
    #     assign_json2 = json_factory("command_AssignResources_2")
    #     LOGGER.info("Invoking AssignResources command on TMC CentralNode")
    #     pytest.command_result = tmc_helper.assign_resources(assign_json2,**ON_OFF_DEVICE_COMMAND_DICT)
    #     LOGGER.info("AssignResources command is invoked successfully")
    # except Exception as ex:
    #     assert "StateModelError" in str(ex)
    #     pytest.command_result = "StateModelError"


# @then(parsers.parse("Subarray remains in {initial_obsstate}"))
# def command_responce(initial_obsstate):
#     resource(tmc_subarraynode1).assert_attribute("obsState").equals(initial_obsstate)
#     LOGGER.info("Done checking for Subarraynode obsstate")


@then(parsers.parse("TMC Subarray remains in {initial_obsstate} and TMC accepts next command {next_command}"))
def tmc_accepts_next_commands(json_factory, initial_obsstate, next_command):
    # resource(tmc_subarraynode1).assert_attribute("obsState").equals(initial_obsstate)
    LOGGER.info("Done checking for Subarraynode obsstate")
    configure_json = json_factory("command_Configure")
    telescope_control = TelescopeControlMid()
    # if next_command == "Configure":
        # Invoke Configure() Command on TMC
    LOGGER.info("Waiting for obsState as IDLE")
    # dic_val = {"sdp_subarray":sdp_subarray1, "csp_subarray":csp_subarray1,"tmc_subarraynode":tmc_subarraynode1}
    # the_waiter = Waiter(kwargs=dic_val)
    # LOGGER.info("Set for wait")
    # the_waiter.set_wait_for_assign_resources()
    LOGGER.info("Invoking Configure command on TMC SubarrayNode")
    tmc_helper.configure_sub(configure_json,**ON_OFF_DEVICE_COMMAND_DICT)
    # tmc_helper.configure_subarray(configure_json,**ON_OFF_DEVICE_COMMAND_DICT)

        # dic_val = {"sdp_subarray":sdp_subarray1, "csp_subarray":csp_subarray1,"tmc_subarraynode":tmc_subarraynode1}
        # the_waiter = Waiter(kwargs=dic_val)
        # the_waiter.set_wait_for_assign_resources()
    # try:
    #     LOGGER.info("Invoking Configure command on TMC SubarrayNode")
    #     # @wait_assign()
    #     # @sync_configure()
    #     def configure_subarray(configure_json):
    #         resource(tmc_subarraynode1).assert_attribute("obsState").equals(
    #             "IDLE"
    #         )
    #         subarray_node = DeviceProxy(tmc_subarraynode1)
    #         subarray_node.Configure(configure_json)
    #         LOGGER.info("Invoked Configure on SubarrayNode")
    #     configure_subarray()
    #     # Verify ObsState is READY

    LOGGER.info("Configure command on TMC SubarrayNode is successful")
    assert telescope_control.is_in_valid_state(DEVICE_OBS_STATE_READY_INFO, "obsState")
    release_json = json_factory("command_ReleaseResources")
    tear_down(release_json)