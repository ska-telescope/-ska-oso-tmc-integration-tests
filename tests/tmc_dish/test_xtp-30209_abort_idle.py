"""Test TMC-DISH Abort functionality in IDLE obstate"""

import time

import pytest
from pytest_bdd import given, parsers, scenario, then, when
from ska_tango_base.control_model import ObsState
from tango import DevState

from tests.resources.test_harness.utils.enums import SimulatorDeviceType
from tests.resources.test_support.enum import DishMode, PointingState


@pytest.mark.skip
@pytest.mark.tmc_dish
@scenario(
    "../features/tmc_dish/xtp-30209_abort_idle.feature",
    "TMC executes Abort command on DISH.LMC when TMC Subarray is in IDLE",
)
def test_tmc_dish_abort_in_idle():
    """
    Test case to verify TMC-DISH Abort functionality in IDLE obsState

    Glossary:
        - "central_node_mid": fixture for a TMC CentralNode under test
        - "simulator_factory": fixture for SimulatorFactory class,
        which provides simulated master devices
        - "event_recorder": fixture for EventRecorder class
    """


@given(
    parsers.parse(
        "a Telescope consisting of TMC, DISH {dish_ids},"
        + " simulated CSP and simulated SDP"
    )
)
def given_a_telescope(
    central_node_mid, simulator_factory, event_recorder, dish_ids
):
    """
    Given a TMC
    """
    csp_master_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.MID_CSP_MASTER_DEVICE
    )
    sdp_master_sim = simulator_factory.get_or_create_simulator_device(
        SimulatorDeviceType.MID_SDP_MASTER_DEVICE
    )
    event_recorder.subscribe_event(csp_master_sim, "State")
    event_recorder.subscribe_event(sdp_master_sim, "State")

    assert csp_master_sim.ping() > 0
    assert sdp_master_sim.ping() > 0
    for dish_id in dish_ids.split(","):
        assert central_node_mid.dish_master_dict[dish_id].ping() > 0


@given("the Telescope is in ON state")
def turn_on_telescope(central_node_mid, event_recorder):
    """A method to put DISH to ON"""
    event_recorder.subscribe_event(
        central_node_mid.dish_master_dict["dish001"], "dishMode"
    )
    event_recorder.subscribe_event(
        central_node_mid.dish_master_dict["dish036"], "dishMode"
    )
    event_recorder.subscribe_event(
        central_node_mid.dish_master_dict["dish063"], "dishMode"
    )
    # event_recorder.subscribe_event(
    #     central_node_mid.dish_master_dict["dish100"], "dishMode"
    # )

    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_master_dict["dish001"],
        "dishMode",
        DishMode.STANDBY_LP,
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_master_dict["dish036"],
        "dishMode",
        DishMode.STANDBY_LP,
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_master_dict["dish063"],
        "dishMode",
        DishMode.STANDBY_LP,
    )
    # assert event_recorder.has_change_event_occurred(
    #     central_node_mid.dish_master_dict["dish100"],
    #     "dishMode",
    #     DishMode.STANDBY_LP,
    # )

    # Wait for the DishLeafNode to get StandbyLP event form DishMaster before
    # invoking TelescopeOn command
    time.sleep(2)

    event_recorder.subscribe_event(
        central_node_mid.central_node, "telescopeState"
    )

    assert event_recorder.has_change_event_occurred(
        central_node_mid.central_node,
        "telescopeState",
        DevState.OFF,
    )
    central_node_mid.move_to_on()

    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_master_dict["dish001"],
        "dishMode",
        DishMode.STANDBY_FP,
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_master_dict["dish036"],
        "dishMode",
        DishMode.STANDBY_FP,
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.dish_master_dict["dish063"],
        "dishMode",
        DishMode.STANDBY_FP,
    )
    # assert event_recorder.has_change_event_occurred(
    #     central_node_mid.dish_master_dict["dish100"],
    #     "dishMode",
    #     DishMode.STANDBY_FP,
    # )

    # Wait for the DishLeafNode to get StandbyFP event form DishMaster before
    # invoking TelescopeOn command
    time.sleep(2)

    assert event_recorder.has_change_event_occurred(
        central_node_mid.sdp_master,
        "State",
        DevState.ON,
    )

    assert event_recorder.has_change_event_occurred(
        central_node_mid.csp_master,
        "State",
        DevState.ON,
    )
    assert event_recorder.has_change_event_occurred(
        central_node_mid.central_node,
        "telescopeState",
        DevState.ON,
    )


@given(parsers.parse("TMC subarray {subarray_id}  is in IDLE ObsState"))
def subarray_is_in_idle_obsstate(
    subarray_node,
    event_recorder,
    subarray_id,
):
    subarray_node.set_subarray_id(subarray_id)

    event_recorder.subscribe_event(subarray_node.subarray_node, "obsState")
    event_recorder.subscribe_event(
        subarray_node.subarray_devices.get("sdp_subarray"), "obsState"
    )
    event_recorder.subscribe_event(
        subarray_node.sdp_subarray_leaf_node, "sdpSubarrayObsState"
    )
    event_recorder.subscribe_event(
        subarray_node.subarray_devices.get("csp_subarray"), "obsState"
    )
    event_recorder.subscribe_event(
        subarray_node.csp_subarray_leaf_node, "cspSubarrayObsState"
    )

    subarray_node.force_change_of_obs_state("IDLE")

    assert event_recorder.has_change_event_occurred(
        subarray_node.subarray_node,
        "obsState",
        ObsState.IDLE,
    )
    assert event_recorder.has_change_event_occurred(
        subarray_node.subarray_devices.get("sdp_subarray"),
        "obsState",
        ObsState.IDLE,
    )
    assert event_recorder.has_change_event_occurred(
        subarray_node.sdp_subarray_leaf_node,
        "sdpSubarrayObsState",
        ObsState.IDLE,
    )
    assert event_recorder.has_change_event_occurred(
        subarray_node.subarray_devices.get("csp_subarray"),
        "obsState",
        ObsState.IDLE,
    )
    assert event_recorder.has_change_event_occurred(
        subarray_node.csp_subarray_leaf_node,
        "cspSubarrayObsState",
        ObsState.IDLE,
    )


@when("I issue the Abort command to the TMC subarray")
def abort_is_invoked(subarray_node):
    """
    This method invokes abort command on tmc subarray.
    """
    subarray_node.abort_subarray()


@then(
    parsers.parse(
        "the DishMaster {dish_ids} transitions to dishMode"
        + " OPERATE and pointingState READY"
    )
)
def check_dish_mode_and_pointing_state(
    central_node_mid, event_recorder, dish_ids
):
    """
    Method to check dishMode and pointingState of DISH
    """
    for dish_id in dish_ids.split(","):
        event_recorder.subscribe_event(
            central_node_mid.dish_master_dict[dish_id], "pointingState"
        )

        assert event_recorder.has_change_event_occurred(
            central_node_mid.dish_master_dict[dish_id],
            "dishMode",
            DishMode.OPERATE,
        )

        assert event_recorder.has_change_event_occurred(
            central_node_mid.dish_master_dict[dish_id],
            "pointState",
            PointingState.READY,
        )


@then("the TMC subarray transitions to ObsState ABORTED")
def tmc_subarray_is_in_aborted_obsstate(subarray_node, event_recorder):
    """
    Method to check if TMC subarray is in ABORTED obsstate
    """
    assert event_recorder.has_change_event_occurred(
        subarray_node.subarray_node,
        "obsState",
        ObsState.ABORTED,
    )
