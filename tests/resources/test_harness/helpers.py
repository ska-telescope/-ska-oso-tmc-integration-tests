from typing import Any, Optional

from tests.conftest import LOGGER
from tests.resources.test_harness.utils.enums import MockDeviceType
from tests.resources.test_harness.utils.wait_helpers import Waiter
from tests.resources.test_support.common_utils.common_helpers import resource
from tests.resources.test_support.constant import (
    csp_subarray1,
    dish_master1,
    dish_master2,
    sdp_subarray1,
    tmc_subarraynode1,
)


def check_subarray_obs_state(obs_state=None, timeout=50):

    device_dict = {
        "sdp_subarray": sdp_subarray1,
        "csp_subarray": csp_subarray1,
        "tmc_subarraynode": tmc_subarraynode1,
    }

    LOGGER.info(
        f"{tmc_subarraynode1}.obsState : "
        + str(resource(tmc_subarraynode1).get("obsState"))
    )
    LOGGER.info(
        f"{sdp_subarray1}.obsState : "
        + str(resource(sdp_subarray1).get("obsState"))
    )
    LOGGER.info(
        f"{csp_subarray1}.obsState : "
        + str(resource(csp_subarray1).get("obsState"))
    )
    if obs_state == "READY":
        device_dict["dish_master_list"] = [dish_master1, dish_master2]
    the_waiter = Waiter(**device_dict)
    the_waiter.set_wait_for_obs_state(obs_state=obs_state)
    the_waiter.wait(timeout / 0.1)

    return all(
        [
            resource(sdp_subarray1).get("obsState") == obs_state,
            resource(tmc_subarraynode1).get("obsState") == obs_state,
            resource(csp_subarray1).get("obsState") == obs_state,
        ]
    )


def tear_down(
    central_node,
    input_json: Optional[str] = None,
    raise_exception: Optional[bool] = True,
):
    """Tears down the system after test run to get telescope back in standby
    state."""
    subarray_node_obsstate = resource(tmc_subarraynode1).get("obsState")

    if subarray_node_obsstate == "IDLE":
        LOGGER.info("Invoking ReleaseResources on TMC")
        central_node.invoke_release_resources(input_json)

        LOGGER.info("Invoking Telescope Standby on TMC")
        central_node.move_off()


def get_device_mocks(mock_factory):
    """A method to get mocks for Subsystem devices


    Args:
        mock_factory (fixture): fixture for MockFactory class

    Returns:
        mock objects
    """
    sdp_mock = mock_factory.get_or_create_mock_device(
        MockDeviceType.SDP_DEVICE
    )
    csp_mock = mock_factory.get_or_create_mock_device(
        MockDeviceType.CSP_DEVICE
    )
    dish_mock_1 = mock_factory.get_or_create_mock_device(
        MockDeviceType.DISH_DEVICE, mock_number=1
    )
    dish_mock_2 = mock_factory.get_or_create_mock_device(
        MockDeviceType.DISH_DEVICE, mock_number=2
    )
    return csp_mock, sdp_mock, dish_mock_1, dish_mock_2


def prepare_json_args_for_commands(args_for_command, command_input_factory):
    if args_for_command is not None:
        input_json = command_input_factory.create_subarray_configuration(
            args_for_command
        )
    else:
        input_json = None
    return input_json


def get_command_call_info(device: Any):
    """
    device: Tango Device Proxy Object

    """
    command_call_info = device.read_attribute("commandCallInfo").value
    LOGGER.info("Command info %s", command_call_info)
    input_str = "".join(command_call_info[0][1].split())
    received_command_call_data = (
        command_call_info[0][0],
        sorted(input_str),
    )
    return received_command_call_data


def device_is_with_correct_command_recorder_data(
    device: Any, expected_command_name: str, expected_inp_str: str
):
    """_summary_"""

    received_command_call_data = get_command_call_info(device)

    expected_input_str = "".join(expected_inp_str.split())

    return received_command_call_data == (
        expected_command_name,
        sorted(expected_input_str),
    )


def single_command_entry_in_command_data(device: Any):
    command_call_info = device.read_attribute("commandCallInfo").value
    return len(command_call_info) == 1
