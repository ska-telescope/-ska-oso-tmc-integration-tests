import pytest
from ska_tango_base.control_model import ObsState

from tests.resources.test_harness.helpers import get_device_simulators


class TestSubarrayNodeAbortCommandObsStateTransitions(object):
    @pytest.mark.parametrize(
        "source_obs_state",
        [
            "IDLE",
            # "SCANNING",
            "READY",
            # "RESOURCING",
            # "CONFIGURING",
        ],
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
        - "simulator_factory": fixture for SimulatorFactory class
        - "source_obs_state": a TMC SubarrayNode initial allowed obsState,
           required to invoke Abort command
        """
        csp_sim, sdp_sim, _, _ = get_device_simulators(simulator_factory)

        event_recorder.subscribe_event(subarray_node.subarray_node, "obsState")
        event_recorder.subscribe_event(csp_sim, "commandCallInfo")
        event_recorder.subscribe_event(sdp_sim, "commandCallInfo")

        subarray_node.move_to_on()
        subarray_node.force_change_of_obs_state(source_obs_state)

        subarray_node.execute_transition("Abort", argin=None)

        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node, "obsState", ObsState.ABORTING
        )
        assert event_recorder.has_change_event_occurred(
            subarray_node.subarray_node, "obsState", ObsState.ABORTED
        )
