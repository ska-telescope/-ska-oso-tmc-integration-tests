from typing import Any

from tests.conftest import LOGGER
from tests.resources.test_harness.utils.common_utils import JsonFactory
from tests.resources.test_harness.utils.enums import SimulatorDeviceType
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


def get_device_simulators(simulator_factory):
    """A method to get simulators for Subsystem devices

    Args:
        simulator_factory (fixture): fixture for SimulatorFactory class

    Returns:
        simulator(sim) objects
    """
    sdp_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.SDP_DEVICE
    )
    csp_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.CSP_DEVICE
    )
    dish_sim_1 = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.DISH_DEVICE, sim_number=1
    )
    dish_sim_2 = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.DISH_DEVICE, sim_number=2
    )
    return csp_sim, sdp_sim, dish_sim_1, dish_sim_2


def get_master_device_simulators(simulator_factory):
    """A method to get simulators for Subsystem master devices

    Args:
        simulator_factory (fixture): fixture for SimulatorFactory class

    Returns:
        simulator(sim) objects
    """
    csp_master_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.CSP_MASTER_DEVICE
    )
    sdp_master_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.SDP_MASTER_DEVICE
    )
    dish_master_sim_1 = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.DISH_DEVICE, sim_number=1
    )

    dish_master_sim_2 = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.DISH_DEVICE, sim_number=2
    )

    return csp_master_sim, sdp_master_sim, dish_master_sim_1, dish_master_sim_2


def get_device_simulator_with_given_name(simulator_factory, devices):
    """Get Device type based on device name and return device proxy
    Args:
        devices (_type_): _description_
    """
    device_name_type_dict = {
        "csp_device": SimulatorDeviceType.CSP_DEVICE,
        "sdp_device": SimulatorDeviceType.SDP_DEVICE,
        "csp master": SimulatorDeviceType.CSP_MASTER_DEVICE,
        "sdp master": SimulatorDeviceType.SDP_MASTER_DEVICE,
    }
    device_proxy_list = []
    for device_name in devices:
        if device_name in device_name_type_dict:
            sim_device_type = device_name_type_dict[device_name]
            device_proxy_list.append(
                simulator_factory.get_or_create_simulator_device(
                    sim_device_type
                )
            )
        elif device_name.startswith("Dish"):
            sim_number = device_name.split()[-1]
            device_proxy_list.append(
                simulator_factory.get_or_create_simulator_device(
                    SimulatorDeviceType.DISH_DEVICE, sim_number=int(sim_number)
                )
            )
    return device_proxy_list


def prepare_json_args_for_commands(
    args_for_command: str, command_input_factory: JsonFactory
) -> str:
    """This method return input json based on command args"""
    if args_for_command is not None:
        input_json = command_input_factory.create_subarray_configuration(
            args_for_command
        )
    else:
        input_json = None
    return input_json


def get_command_call_info(device: Any, command_name: str):
    """
    device: Tango Device Proxy Object

    """
    command_call_info = device.read_attribute("commandCallInfo").value
    LOGGER.info("Command info %s", command_call_info)
    command_info = [
        command_info
        for command_info in command_call_info
        if command_info[0] == command_name
    ]
    # if command_info[0][1] != "":
    input_str = "".join(command_info[0][1].split())
    received_command_call_data = (
        command_call_info[0][0],
        sorted(input_str),
    )
    return received_command_call_data
    # else:
    #     received_command_call_data = (command_call_info[0][0], "")
    #     return received_command_call_data


def device_received_this_command(
    device: Any, expected_command_name: str, expected_inp_str: str
):
    """Method to verify received command and command argument

    Args:
        device (Any): Tango Device Proxy Object
        expected_command_name (str): Command name received on simulator device
        expected_inp_str (str): Command argument received on simulator device

    Returns:
        Boolean: True if received data is equal to expected data.
    """
    received_command_call_data = get_command_call_info(
        device, expected_command_name
    )
    # if expected_inp_str is not None:
    expected_input_str = "".join(expected_inp_str.split())

    return received_command_call_data == (
        expected_command_name,
        sorted(expected_input_str),
    )
    # else:
    #     return received_command_call_data == (
    #         expected_command_name,
    #         "",
    #     )


def get_recorded_commands(device: Any):
    """A method to get data from simulator device

    Args:
        device (Any): Tango Device Proxy Object

    Returns: List[tuple]
        recorded data from Simulator device
    """
    return device.read_attribute("commandCallInfo").value
