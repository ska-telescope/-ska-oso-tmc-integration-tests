import json
import logging

import msgpack
import msgpack_numpy
from ska_control_model import ObsState
from ska_ser_logging import configure_logging
from ska_tango_base.control_model import HealthState
from tango import DeviceProxy, DevState

from tests.resources.test_harness.constant import (
    POINTING_OFFSETS,
    centralnode,
    csp_master,
    csp_subarray1,
    dish_master1,
    dish_master2,
    sdp_master,
    sdp_queue_connector,
    sdp_subarray1,
    tmc_csp_subarray_leaf_node,
    tmc_dish_leaf_node1,
    tmc_dish_leaf_node2,
    tmc_sdp_subarray_leaf_node,
    tmc_subarraynode1,
)
from tests.resources.test_harness.helpers import (
    SIMULATED_DEVICES_DICT,
    check_subarray_obs_state,
    prepare_json_args_for_commands,
)
from tests.resources.test_harness.utils.constant import (
    ABORTED,
    IDLE,
    ON,
    READY,
)
from tests.resources.test_harness.utils.enums import DishMode, SubarrayObsState
from tests.resources.test_harness.utils.obs_state_resetter import (
    ObsStateResetterFactory,
)
from tests.resources.test_harness.utils.sync_decorators import (
    sync_abort,
    sync_assign_resources,
    sync_configure,
    sync_end,
    sync_endscan,
    sync_release_resources,
    sync_restart,
)
from tests.resources.test_support.common_utils.common_helpers import Resource

configure_logging(logging.DEBUG)
LOGGER = logging.getLogger(__name__)

device_dict = {
    # TODO use this as as list when multiple subarray considered in testing
    "sdp_subarray": sdp_subarray1,
    "csp_subarray": csp_subarray1,
    "csp_master": csp_master,
    "tmc_subarraynode": tmc_subarraynode1,
    "sdp_master": sdp_master,
    "centralnode": centralnode,
    "dish_master_list": [dish_master1, dish_master2],
    "csp_subarray_leaf_node": tmc_csp_subarray_leaf_node,
    "sdp_subarray_leaf_node": tmc_sdp_subarray_leaf_node,
}


class SubarrayNodeWrapper(object):
    """Subarray Node class which implement methods required for test cases
    to test subarray node.
    """

    def __init__(self) -> None:
        super().__init__()
        self.tmc_subarraynode1 = tmc_subarraynode1
        self.subarray_node = DeviceProxy(self.tmc_subarraynode1)
        self.csp_subarray_leaf_node = DeviceProxy(tmc_csp_subarray_leaf_node)
        self.sdp_subarray_leaf_node = DeviceProxy(tmc_sdp_subarray_leaf_node)
        self.dish_leaf_node_list = [
            DeviceProxy(tmc_dish_leaf_node1),
            DeviceProxy(tmc_dish_leaf_node2),
        ]
        self.dish_master_list = [
            DeviceProxy(dish_master1),
            DeviceProxy(dish_master2),
        ]
        self.subarray_devices = {
            "csp_subarray": DeviceProxy(csp_subarray1),
            "sdp_subarray": DeviceProxy(sdp_subarray1),
        }

        self._state = DevState.OFF
        self.obs_state = SubarrayObsState.EMPTY
        # setup subarray
        self._setup()
        # Subarray state
        self.ON_STATE = ON
        self.IDLE_OBS_STATE = IDLE
        self.READY_OBS_STATE = READY
        self.ABORTED_OBS_STATE = ABORTED
        self.csp_subarray1 = csp_subarray1
        self.sdp_subarray1 = sdp_subarray1

    def _setup(self):
        """ """
        for dish_master_proxy in self.dish_master_list:
            dish_master_proxy.SetDirectState(DevState.STANDBY)
            # Setting DishMode to STANDBY_FP
            dish_master_proxy.SetDirectDishMode(DishMode.STANDBY_FP)

    @property
    def state(self) -> DevState:
        """TMC SubarrayNode operational state"""
        self._state = Resource(self.tmc_subarraynode1).get("State")
        return self._state

    @state.setter
    def state(self, value):
        """Sets value for TMC subarrayNode operational state

        Args:
            value (DevState): operational state value
        """
        self._state = value

    @property
    def obs_state(self):
        """TMC SubarrayNode observation state"""
        self._obs_state = Resource(self.tmc_subarraynode1).get("obsState")
        return self._obs_state

    @obs_state.setter
    def obs_state(self, value):
        """Sets value for TMC subarrayNode observation state

        Args:
            value (DevState): observation state value
        """
        self._obs_state = value

    @property
    def health_state(self) -> HealthState:
        """Telescope health state representing overall health of telescope"""
        self._health_state = Resource(self.tmc_subarraynode1).get(
            "healthState"
        )
        return self._health_state

    @health_state.setter
    def health_state(self, value):
        """Telescope health state representing overall health of telescope

        Args:
            value (HealthState): telescope health state value
        """
        self._health_state = value

    def move_to_on(self):
        # Move subarray to ON state
        if self.state != self.ON_STATE:
            Resource(self.tmc_subarraynode1).assert_attribute("State").equals(
                "OFF"
            )
            result, message = self.subarray_node.On()
            LOGGER.info("Invoked ON on SubarrayNode")
            return result, message

    def move_to_off(self):
        # Move Subarray to OFF state
        Resource(self.tmc_subarraynode1).assert_attribute("State").equals("ON")
        result, message = self.subarray_node.Off()
        LOGGER.info("Invoked OFF on SubarrayNode")
        return result, message

    @sync_configure(device_dict=device_dict)
    def store_configuration_data(self, input_string: str):
        """Invoke configure command on subarray Node
        Args:
            input_string (str): config input json
        Returns:
            (result, message): result, message tuple
        """
        result, message = self.subarray_node.Configure(input_string)
        LOGGER.info("Invoked Configure on SubarrayNode")
        return result, message

    @sync_end(device_dict=device_dict)
    def end_observation(self):
        result, message = self.subarray_node.End()
        LOGGER.info("Invoked End on SubarrayNode")
        return result, message

    @sync_endscan(device_dict=device_dict)
    def remove_scan_data(self):
        result, message = self.subarray_node.EndScan()
        LOGGER.info("Invoked EndScan on SubarrayNode")
        return result, message

    def store_scan_data(self, input_string):
        result, message = self.subarray_node.Scan(input_string)
        LOGGER.info("Invoked Scan on SubarrayNode")
        return result, message

    @sync_abort(device_dict=device_dict)
    def abort_subarray(self):
        result, message = self.subarray_node.Abort()
        LOGGER.info("Invoked Abort on SubarrayNode")
        return result, message

    @sync_restart(device_dict=device_dict)
    def restart_subarray(self):
        result, message = self.subarray_node.Restart()
        LOGGER.info("Invoked Restart on SubarrayNode")
        return result, message

    @sync_assign_resources(device_dict)
    def store_resources(self, assign_json: str):
        """Invoke Assign Resource command on subarray Node
        Args:
            assign_json (str): Assign resource input json
        """
        result, message = self.subarray_node.AssignResources(assign_json)
        LOGGER.info("Invoked AssignResources on SubarrayNode")
        return result, message

    @sync_release_resources(device_dict)
    def release_resources_subarray(self):
        result, message = self.subarray_node.ReleaseAllResources()
        LOGGER.info("Invoked Release Resource on SubarrayNode")
        return result, message

    def execute_transition(self, command_name: str, argin=None):
        """Execute provided command on subarray
        Args:
            command_name (str): Name of command to execute
        """
        if command_name is not None:
            result, message = self.subarray_node.command_inout(
                command_name, argin
            )
            LOGGER.info(f"Invoked {command_name} on SubarrayNode")
            return result, message

    def _reset_simulator_devices(self):
        """Reset Simulator devices to it's original state"""
        for sim_device_fqdn in [
            self.sdp_subarray1,
        ]:
            device = DeviceProxy(sim_device_fqdn)
            device.ResetDelay()
            device.SetDirectHealthState(HealthState.UNKNOWN)
            device.SetDefective(json.dumps({"enabled": False}))

    def _reset_dishes(self):
        """Reset Dish Devices"""
        for dish_master in self.dish_master_list:
            dish_master.SetDirectDishMode(DishMode.STANDBY_LP)
            dish_master.SetDirectState(DevState.STANDBY)
            dish_master.ResetDelay()
            dish_master.SetDirectHealthState(HealthState.UNKNOWN)

    def _clear_command_call_and_transition_data(self, clear_transition=False):
        """Clears the command call data"""
        if not SIMULATED_DEVICES_DICT["sdp_and_dish"]:
            for sim_device in [
                self.sdp_subarray1,
                dish_master1,
                dish_master2,
            ]:
                device = DeviceProxy(sim_device)
                device.ClearCommandCallInfo()
                if clear_transition:
                    device.ResetTransitions()

    def tear_down(self):
        """Tear down after each test run"""

        LOGGER.info("Calling Tear down for subarray")
        self._clear_command_call_and_transition_data(clear_transition=True)

        if self.obs_state in ("RESOURCING", "CONFIGURING", "SCANNING"):
            """Invoke Abort and Restart"""
            LOGGER.info("Invoking Abort on Subarray")
            self.abort_subarray()
            self.restart_subarray()
        elif self.obs_state == "ABORTED":
            """Invoke Restart"""
            LOGGER.info("Invoking Restart on Subarray")
            self.restart_subarray()
        else:
            self.force_change_of_obs_state("EMPTY")

        # Move Subarray to OFF state
        self.move_to_off()
        self._reset_dishes()
        self._reset_simulator_devices()
        assert check_subarray_obs_state("EMPTY")

    def clear_all_data(self):
        """Method to clear the observations
        and put the SubarrayNode in EMPTY"""
        if self.obs_state in [
            "IDLE",
            "RESOURCING",
            "READY",
            "CONFIGURING",
            "SCANNING",
        ]:
            self.abort_subarray()
            self.restart_subarray()
        elif self.obs_state == "ABORTED":
            self.restart_subarray()

    def force_change_of_obs_state(
        self,
        dest_state_name: str,
        assign_input_json: str = "",
        configure_input_json: str = "",
        scan_input_json: str = "",
    ) -> None:
        """Force SubarrayNode obsState to provided obsState

        Args:
            dest_state_name (str): Destination obsState
        """
        factory_obj = ObsStateResetterFactory()
        obs_state_resetter = factory_obj.create_obs_state_resetter(
            dest_state_name, self
        )
        if assign_input_json:
            obs_state_resetter.assign_input = assign_input_json
        if configure_input_json:
            obs_state_resetter.configure_input = configure_input_json
        if scan_input_json:
            obs_state_resetter.scan_input = scan_input_json
        obs_state_resetter.reset()
        self._clear_command_call_and_transition_data()

    def simulate_receive_addresses_event(self, sdp_sim, command_input_factory):
        """Sets the receive addresses attribute on SDP Subarray so an event can
        be simulated for Subarray Node to process.
        """
        receive_addresses = prepare_json_args_for_commands(
            "receive_addresses_mid", command_input_factory
        )
        sdp_sim.SetDirectreceiveAddresses(receive_addresses)

        # Setting pointing offsets after encoding the data.
        sdp_qc = DeviceProxy(sdp_queue_connector)
        encoded_data = msgpack.packb(
            POINTING_OFFSETS, default=msgpack_numpy.encode
        )
        sdp_qc.SetDirectPointingOffsets(("msgpack_numpy", encoded_data))

    def execute_five_point_calibration_scan(
        self,
        partial_configure_jsons: list[str],
        scan_jsons: list[str],
        event_recorder,
        command_input_factory,
    ) -> None:
        """Perform a five point calibration scan on Subarray Node using the
        partial configuration jsons and scan jsons provided as inputs.

        Args:
            partial_configure_jsons (list[str]): Partial configuration json
                file names
            scan_jsons (list[str]): Scan json file names
        """
        partial_configure_1 = prepare_json_args_for_commands(
            partial_configure_jsons[0], command_input_factory
        )
        partial_configure_2 = prepare_json_args_for_commands(
            partial_configure_jsons[1], command_input_factory
        )
        partial_configure_3 = prepare_json_args_for_commands(
            partial_configure_jsons[2], command_input_factory
        )
        partial_configure_4 = prepare_json_args_for_commands(
            partial_configure_jsons[3], command_input_factory
        )

        scan_1 = prepare_json_args_for_commands(
            scan_jsons[0], command_input_factory
        )
        scan_2 = prepare_json_args_for_commands(
            scan_jsons[1], command_input_factory
        )
        scan_3 = prepare_json_args_for_commands(
            scan_jsons[2], command_input_factory
        )
        scan_4 = prepare_json_args_for_commands(
            scan_jsons[3], command_input_factory
        )

        # Partial configure 1
        self.execute_transition("Configure", partial_configure_1)
        assert event_recorder.has_change_event_occurred(
            self.subarray_node,
            "obsState",
            ObsState.CONFIGURING,
            lookahead=15,
        )
        assert check_subarray_obs_state(obs_state="READY")

        # Scan 1
        self.execute_transition("Scan", scan_1)
        assert event_recorder.has_change_event_occurred(
            self.subarray_node,
            "obsState",
            ObsState.SCANNING,
            lookahead=15,
        )
        assert check_subarray_obs_state(obs_state="READY")

        # Partial configure 2
        self.execute_transition("Configure", partial_configure_2)
        assert event_recorder.has_change_event_occurred(
            self.subarray_node,
            "obsState",
            ObsState.CONFIGURING,
            lookahead=15,
        )
        assert check_subarray_obs_state(obs_state="READY")

        # Scan 2
        self.execute_transition("Scan", scan_2)
        assert event_recorder.has_change_event_occurred(
            self.subarray_node,
            "obsState",
            ObsState.SCANNING,
            lookahead=15,
        )
        assert check_subarray_obs_state(obs_state="READY")

        # Partial configure 3
        self.execute_transition("Configure", partial_configure_3)
        assert event_recorder.has_change_event_occurred(
            self.subarray_node,
            "obsState",
            ObsState.CONFIGURING,
            lookahead=15,
        )
        assert check_subarray_obs_state(obs_state="READY")

        # Scan 3
        self.execute_transition("Scan", scan_3)
        assert event_recorder.has_change_event_occurred(
            self.subarray_node,
            "obsState",
            ObsState.SCANNING,
            lookahead=15,
        )
        assert check_subarray_obs_state(obs_state="READY")

        # Partial configure 4
        self.execute_transition("Configure", partial_configure_4)
        assert event_recorder.has_change_event_occurred(
            self.subarray_node,
            "obsState",
            ObsState.CONFIGURING,
            lookahead=15,
        )
        assert check_subarray_obs_state(obs_state="READY")

        # Scan 4
        self.execute_transition("Scan", scan_4)
        assert event_recorder.has_change_event_occurred(
            self.subarray_node,
            "obsState",
            ObsState.SCANNING,
            lookahead=15,
        )
        assert check_subarray_obs_state("READY")
