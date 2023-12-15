import json
import logging
import time
from typing import Any

import pytest
from ska_control_model import ObsState
from ska_ser_logging import configure_logging
from ska_tango_base.commands import ResultCode
from ska_tango_base.control_model import HealthState
from ska_tango_testing.mock.placeholders import Anything
from tango import DeviceProxy

from tests.resources.test_harness.utils.common_utils import JsonFactory
from tests.resources.test_harness.utils.enums import SimulatorDeviceType
from tests.resources.test_harness.utils.wait_helpers import Waiter, watch
from tests.resources.test_support.common_utils.common_helpers import Resource
from tests.resources.test_support.constant import (
    INTERMEDIATE_CONFIGURING_OBS_STATE_DEFECT,
    INTERMEDIATE_STATE_DEFECT,
    csp_subarray1,
    dish_master1,
    dish_master2,
    sdp_subarray1,
    tmc_csp_subarray_leaf_node,
    tmc_sdp_subarray_leaf_node,
    tmc_subarraynode1,
)
from tests.resources.test_support.constant_low import (
    csp_subarray1 as csp_subarray1_low,
)
from tests.resources.test_support.constant_low import (
    sdp_subarray1 as sdp_subarray1_low,
)

configure_logging(logging.DEBUG)
LOGGER = logging.getLogger(__name__)
TIMEOUT = 20


def check_subarray_obs_state(obs_state=None, timeout=50):
    device_dict = {
        "sdp_subarray": sdp_subarray1,
        "csp_subarray": csp_subarray1,
        "tmc_subarraynode": tmc_subarraynode1,
        "csp_subarray_leaf_node": tmc_csp_subarray_leaf_node,
        "sdp_subarray_leaf_node": tmc_sdp_subarray_leaf_node,
    }

    LOGGER.info(
        f"{tmc_subarraynode1}.obsState : "
        + str(Resource(tmc_subarraynode1).get("obsState"))
    )
    LOGGER.info(
        f"{sdp_subarray1}.obsState : "
        + str(Resource(sdp_subarray1).get("obsState"))
    )
    LOGGER.info(
        f"{csp_subarray1}.obsState : "
        + str(Resource(csp_subarray1).get("obsState"))
    )
    if obs_state == "READY":
        device_dict["dish_master_list"] = [dish_master1, dish_master2]
    the_waiter = Waiter(**device_dict)
    the_waiter.set_wait_for_obs_state(obs_state=obs_state)
    the_waiter.wait(timeout / 0.1)

    return all(
        [
            Resource(sdp_subarray1).get("obsState") == obs_state,
            Resource(tmc_subarraynode1).get("obsState") == obs_state,
            Resource(csp_subarray1).get("obsState") == obs_state,
        ]
    )


def get_device_simulators(simulator_factory):
    """A method to get simulators for Subsystem devices

    Args:
        simulator_factory (fixture): fixture for SimulatorFactory class,
        which provides simulated subarray and master devices

    Returns:
        simulator(sim) objects
    """
    sdp_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.MID_SDP_DEVICE
    )
    csp_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.MID_CSP_DEVICE
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
        simulator_factory (fixture): fixture for SimulatorFactory class,
        which provides simulated subarray and master devices

    Returns:
        simulator(sim) objects
    """
    csp_master_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.MID_CSP_MASTER_DEVICE
    )
    sdp_master_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.MID_SDP_MASTER_DEVICE
    )
    dish_master_sim_1 = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.DISH_DEVICE, sim_number=1
    )
    dish_master_sim_2 = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.DISH_DEVICE, sim_number=2
    )
    return (
        csp_master_sim,
        sdp_master_sim,
        dish_master_sim_1,
        dish_master_sim_2,
    )


def get_device_simulator_with_given_name(simulator_factory, devices):
    """Get Device type based on device name and return device proxy
    Args:
        devices (list): simulator devices list
    """
    device_name_type_dict = {
        "csp subarray": SimulatorDeviceType.MID_CSP_DEVICE,
        "sdp subarray": SimulatorDeviceType.MID_SDP_DEVICE,
        "csp master": SimulatorDeviceType.MID_CSP_MASTER_DEVICE,
        "sdp master": SimulatorDeviceType.MID_SDP_MASTER_DEVICE,
    }
    sim_device_proxy_list = []
    for device_name in devices:
        if device_name in device_name_type_dict:
            sim_device_type = device_name_type_dict[device_name]
            sim_device_proxy_list.append(
                simulator_factory.get_or_create_simulator_device(
                    sim_device_type
                )
            )
        elif device_name.startswith("dish"):
            sim_number = device_name.split()[-1]
            sim_device_proxy_list.append(
                simulator_factory.get_or_create_simulator_device(
                    SimulatorDeviceType.DISH_DEVICE, sim_number=int(sim_number)
                )
            )
    return sim_device_proxy_list


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


def prepare_json_args_for_centralnode_commands(
    args_for_command: str, command_input_factory: JsonFactory
) -> str:
    """This method return input json based on command args"""
    if args_for_command is not None:
        input_json = command_input_factory.create_centralnode_configuration(
            args_for_command
        )
    else:
        input_json = None
    return input_json


def get_command_call_info_boolean(device: Any, command_name: str):
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

    received_command_call_data = (
        command_call_info[0][0],
        command_info[0][1],
    )

    return received_command_call_data


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

    LOGGER.info("command_info[0][1] - %s", command_info[0][1])
    LOGGER.info("command_info[0][1] - %s", type(command_info[0][1]))

    input_str = json.loads("".join(command_info[0][1].split()))

    received_command_call_data = (
        command_call_info[0][0],
        sorted(input_str),
    )

    return received_command_call_data


def set_subarray_to_given_obs_state(
    subarray_node: DeviceProxy,
    obs_state: str,
    event_recorder,
    command_input_factory,
):
    """Set the Subarray node to given obsState."""
    # This method with be removed after the helper devices are updated to have
    # a ThreadPoolExecutor.
    match obs_state:
        case "RESOURCING":
            # Setting the device defective
            csp_subarray = DeviceProxy(csp_subarray1_low)
            csp_subarray.SetDefective(json.dumps(INTERMEDIATE_STATE_DEFECT))

            subarray_node.force_change_of_obs_state(obs_state)

            # Waiting for SDP Subarray to go to ObsState.IDLE
            sdp_subarray = DeviceProxy(sdp_subarray1_low)
            event_recorder.subscribe_event(sdp_subarray, "obsState")
            assert event_recorder.has_change_event_occurred(
                sdp_subarray,
                "obsState",
                ObsState.IDLE,
            )
            # Resetting defect on CSP Subarray.
            csp_subarray.SetDefective(json.dumps({"enabled": False}))

        case "CONFIGURING":
            subarray_node.force_change_of_obs_state("IDLE")
            # Setting the device defective
            csp_subarray = DeviceProxy(csp_subarray1_low)
            csp_subarray.SetDefective(
                json.dumps(INTERMEDIATE_CONFIGURING_OBS_STATE_DEFECT)
            )

            configure_input = prepare_json_args_for_commands(
                "configure_low", command_input_factory
            )
            subarray_node.execute_transition("Configure", configure_input)

            # Waiting for SDP Subarray to go to ObsState.READY
            sdp_subarray = DeviceProxy(sdp_subarray1_low)
            event_recorder.subscribe_event(sdp_subarray, "obsState")
            assert event_recorder.has_change_event_occurred(
                sdp_subarray,
                "obsState",
                ObsState.READY,
            )
            # Resetting defect on CSP Subarray.
            csp_subarray.SetDefective(json.dumps({"enabled": False}))


def device_received_this_command(
    device: Any, expected_command_name: str, expected_inp_str: str | bool
):
    """Method to verify received command and command argument

    Args:
        device (Any): Tango Device Proxy Object
        expected_command_name (str): Command name received on simulator device
        expected_inp_str (str): Command argument received on simulator device

    Returns:
        Boolean: True if received data is equal to expected data.
    """

    LOGGER.info("expected_inp_str - %s", expected_inp_str)

    if (
        expected_inp_str == "True"
        or expected_inp_str == "False"
        or expected_inp_str == ""
    ):

        received_command_call_data = get_command_call_info_boolean(
            device, expected_command_name
        )
        LOGGER.info(
            "received_command_call_data - %s", received_command_call_data
        )

        LOGGER.info("expected_inp_str %s", expected_inp_str)
        return received_command_call_data == (
            expected_command_name,
            expected_inp_str,
        )

    else:

        received_command_call_data = get_command_call_info(
            device, expected_command_name
        )
        LOGGER.info(
            "received_command_call_data - %s", received_command_call_data
        )

        expected_input_str = json.loads("".join(expected_inp_str.split()))
        LOGGER.info("expected_input_str %s", expected_input_str)
        return received_command_call_data == (
            expected_command_name,
            sorted(expected_input_str),
        )

    # if type(expected_inp_str) is str:
    #     expected_input_str = json.loads("".join(expected_inp_str.split()))
    #     LOGGER.info("expected_input_str %s", expected_input_str)
    #     return received_command_call_data == (
    #         expected_command_name,
    #         sorted(expected_input_str),
    #     )
    # else:
    #
    #     LOGGER.info("expected_inp_str %s", expected_inp_str)
    #     return received_command_call_data == (
    #         expected_command_name,
    #         expected_inp_str,
    #     )


#
def get_recorded_commands(device: Any):
    """A method to get data from simulator device

    Args:
        device (Any): Tango Device Proxy Object

    Returns: List[tuple]
        recorded data from Simulator device
    """
    return device.read_attribute("commandCallInfo").value


def set_desired_health_state(
    sim_devices_list: list, health_state_value: HealthState
):
    """A method to set simulator devices healthState attribute

    Args:
        sim_devices_list: simulator devices list
        health_state_value: desired healthState value to set
    """

    for device in sim_devices_list:
        device.SetDirectHealthState(health_state_value)
        device.SetDirectHealthState(health_state_value)
        device.SetDirectHealthState(health_state_value)
        device.SetDirectHealthState(health_state_value)


def check_assigned_resources(device: Any, receiptor_ids: tuple):
    """
    Method to verify assignedResources attribute value on subarraynode
    Args:
        device : tango device proxy object.
        receiptor_ids: dish ids.
    """
    assigned_resources = device.read_attribute("assignedResources").value
    LOGGER.info(f"assigned Resources:{assigned_resources}")
    return assigned_resources == receiptor_ids


def device_attribute_changed(
    device: Any,
    attribute_name_list: list,
    attribute_value_list: list,
    timeout: int,
):
    """
    Method to verify device attribute changed to speicified attribute value
    """

    waiter = Waiter()
    for attribute_name, attribute_value in zip(
        attribute_name_list, attribute_value_list
    ):
        waiter.waits.append(
            watch(Resource(device.dev_name())).to_become(
                attribute_name, attribute_value
            )
        )
    try:
        waiter.wait(timeout)
    except Exception:
        return False
    return True


def wait_for_attribute_update(
    device, attribute_name: str, expected_id: str, expected_result: ResultCode
):
    """Wait for the attribute to reflect necessary changes."""
    start_time = time.time()
    elapsed_time = time.time() - start_time
    while elapsed_time <= TIMEOUT:
        unique_id, result = device.read_attribute(attribute_name).value
        if expected_id in unique_id:
            LOGGER.info("The attribute value is: %s, %s", unique_id, result)
            return result == str(expected_result.value)
        time.sleep(1)
        elapsed_time = time.time() - start_time
    return False


def check_lrcr_events(
    event_recorder,
    device,
    command_name: str,
    result_code: ResultCode = ResultCode.OK,
    retries: int = 10,
):
    """Used to assert command name and result code in
       longRunningCommandResult event callbacks.

    Args:
        event_recorder (EventRecorder):fixture used to
        capture event callbacks
        device (str): device for which attribute needs to be checked
        command_name (str): command name to check
        result_code (ResultCode): result_code to check.
        Defaults to ResultCode.OK.
        retries (int):number of events to check. Defaults to 10.
    """
    COUNT = 0
    while COUNT <= retries:
        assertion_data = event_recorder.has_change_event_occurred(
            device, "longRunningCommandResult", Anything, lookahead=1
        )
        unique_id, result = assertion_data["attribute_value"]
        if unique_id.endswith(command_name):
            if result == str(result_code.value):
                LOGGER.debug("TRACKLOADSTATICOFF_UID: %s", unique_id)
                break
        COUNT = COUNT + 1
        if COUNT >= retries:
            pytest.fail("Assertion Failed")
