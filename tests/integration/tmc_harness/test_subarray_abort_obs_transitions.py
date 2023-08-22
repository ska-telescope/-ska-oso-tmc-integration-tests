import pytest
from ska_tango_base.control_model import ObsState
from tango import DeviceProxy

from tests.conftest import LOGGER
from tests.resources.test_harness.constant import (
    tmc_csp_subarray_leaf_node,
    tmc_sdp_subarray_leaf_node,
)
from tests.resources.test_harness.helpers import (
    check_subarray_obs_state,
    get_device_simulators,
)


class TestSubarrayNodeAbortCommandObsStateTransitions(object):
    @pytest.mark.parametrize(
        "source_obs_state",
        ["IDLE", "READY", "SCANNING"],
    )
    @pytest.mark.SKA_mid
    def test_subarray_obs_transitions_valid_data(
        self,
        subarray_node,
        simulator_factory,
        event_recorder,
        source_obs_state,
    ):
        """
        Test to verify transitions that are triggered by Abort
        command and followed by a completion transition
        that start with a transient state.
        assuming that external subsystems work fine.
        Glossary:
        - "subarray_node": fixture for a TMC SubarrayNode under test
        - "simulator_factory": fixture for SimulatorFactory class,
        which provides simulated subarray and master devices
        - "source_obs_state": a TMC SubarrayNode initial allowed obsState,
           required to invoke Abort command
        """

        tmc_csp = DeviceProxy(tmc_csp_subarray_leaf_node)
        tmc_sdp = DeviceProxy(tmc_sdp_subarray_leaf_node)

        event_recorder.subscribe_event(subarray_node.subarray_node, "obsState")
        event_recorder.subscribe_event(tmc_csp, "cspSubarrayObsState")
        event_recorder.subscribe_event(tmc_sdp, "sdpSubarrayObsState")

        subarray_node.move_to_on()
        subarray_node.force_change_of_obs_state(source_obs_state)

        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node, "obsState", ObsState[source_obs_state]
        )

        assert event_recorder.has_change_event_occurred(
            tmc_csp, "cspSubarrayObsState", ObsState[source_obs_state]
        )
        assert event_recorder.has_change_event_occurred(
            tmc_sdp, "sdpSubarrayObsState", ObsState[source_obs_state]
        )

        subarray_node.execute_transition("Abort", argin=None)

        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node, "obsState", ObsState.ABORTING
        )

        assert event_recorder.has_change_event_occurred(
            tmc_sdp, "sdpSubarrayObsState", ObsState.ABORTED
        )
        assert event_recorder.has_change_event_occurred(
            tmc_csp, "cspSubarrayObsState", ObsState.ABORTED
        )
        # assert check_subarray_obs_state(obs_state="ABORTED")
        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node, "obsState", ObsState.ABORTED
        )

    @pytest.mark.parametrize(
        "source_obs_state",
        [
            "CONFIGURING",
            "RESOURCING",
        ],
    )
    @pytest.mark.SKA_mid
    def test_subarray_obs_intermediate_transitions(
        self,
        subarray_node,
        simulator_factory,
        event_recorder,
        source_obs_state,
    ):
        """
        Test to verify transitions that are triggered by Abort
        command and followed by a completion transition
        that start with a transient state.
        assuming that external subsystems work fine.
        Glossary:
        - "subarray_node": fixture for a TMC SubarrayNode under test
        - "simulator_factory": fixture for SimulatorFactory class,
        which provides simulated subarray and master devices
        - "source_obs_state": a TMC SubarrayNode initial allowed obsState,
           required to invoke Abort command
        """
        tmc_csp = DeviceProxy(tmc_csp_subarray_leaf_node)
        tmc_sdp = DeviceProxy(tmc_sdp_subarray_leaf_node)
        csp_sim, sdp_sim, _, _ = get_device_simulators(simulator_factory)

        if source_obs_state == "CONFIGURING":
            obs_state_duration_params = '[["CONFIGURING",0.1]]'
            csp_sim.AddTransition(obs_state_duration_params)
            sdp_sim.AddTransition(obs_state_duration_params)

        event_recorder.subscribe_event(subarray_node.subarray_node, "obsState")
        event_recorder.subscribe_event(tmc_csp, "cspSubarrayObsState")
        event_recorder.subscribe_event(tmc_sdp, "sdpSubarrayObsState")

        subarray_node.move_to_on()
        subarray_node.force_change_of_obs_state(source_obs_state)

        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node, "obsState", ObsState[source_obs_state]
        )

        assert event_recorder.has_change_event_occurred(
            tmc_csp, "cspSubarrayObsState", ObsState[source_obs_state]
        )
        assert event_recorder.has_change_event_occurred(
            tmc_sdp, "sdpSubarrayObsState", ObsState[source_obs_state]
        )

        LOGGER.info(
            "TMC SDP obs State %s",
            tmc_sdp.read_attribute("sdpSubarrayObsState").value,
        )
        LOGGER.info(
            "TMC CSP obs State %s",
            tmc_csp.read_attribute("cspSubarrayObsState").value,
        )

        subarray_node.execute_transition("Abort", argin=None)

        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node, "obsState", ObsState.ABORTING
        )

        LOGGER.info(
            "TMC SDP obs State After %s",
            tmc_sdp.read_attribute("sdpSubarrayObsState").value,
        )
        LOGGER.info(
            "TMC CSP obs State After %s",
            tmc_csp.read_attribute("cspSubarrayObsState").value,
        )

        # assert event_recorder.has_change_event_occurred(
        #     csp_sim, "obsState", ObsState.ABORTING
        # )
        # assert event_recorder.has_change_event_occurred(
        #     sdp_sim, "obsState", ObsState.ABORTING
        # )
        assert event_recorder.has_change_event_occurred(
            tmc_sdp, "sdpSubarrayObsState", ObsState.ABORTED
        )
        assert event_recorder.has_change_event_occurred(
            tmc_csp, "cspSubarrayObsState", ObsState.ABORTED
        )
        # assert check_subarray_obs_state(obs_state="ABORTED")
        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node, "obsState", ObsState.ABORTED
        )
