import pytest
from ska_tango_base.control_model import HealthState

from tests.resources.test_harness.helpers import (
    get_device_simulators,
    get_master_device_simulators,
)


class TestTelescopeHealthState(object):
    """This class implement test cases to verify telescopeHealthState of CentralNode"""

    @pytest.mark.SKA_mid
    def test_telescope_state_unknown(
        self, central_node, simulator_factory, event_recorder
    ):
        csp_master_sim, sdp_master_sim, _, _ = get_master_device_simulators(
            simulator_factory
        )
        csp_master_sim.SetDirectHealthState(HealthState.OK)
        sdp_master_sim.SetDirectHealthState(HealthState.OK)

        event_recorder.subscribe_event(
            central_node.central_node, "telescopeHealthState"
        )

        assert event_recorder.has_change_event_occurred(
            central_node.central_node,
            "telescopeHealthState",
            HealthState.UNKNOWN,
        )

    @pytest.mark.SKA_mid
    def test_telescope_state_degraded(
        self, central_node, simulator_factory, event_recorder
    ):
        csp_master_sim, sdp_master_sim, _, _ = get_master_device_simulators(
            simulator_factory
        )
        csp_master_sim.SetDirectHealthState(HealthState.OK)
        sdp_master_sim.SetDirectHealthState(HealthState.DEGRADED)

        event_recorder.subscribe_event(
            central_node.central_node, "telescopeHealthState"
        )

        assert event_recorder.has_change_event_occurred(
            central_node.central_node,
            "telescopeHealthState",
            HealthState.DEGRADED,
        )

    @pytest.mark.skip(reason="WIP")
    @pytest.mark.SKA_mid
    def test_telescope_state_ok(
        self, central_node, subarray_node, simulator_factory, event_recorder
    ):
        csp_master_sim, sdp_master_sim, _, _ = get_master_device_simulators(
            simulator_factory
        )

        self.set_subarray_health_state_as_OK(subarray_node, simulator_factory)

        csp_master_sim.SetDirectHealthState(HealthState.OK)
        sdp_master_sim.SetDirectHealthState(HealthState.OK)

        event_recorder.subscribe_event(
            central_node.central_node, "telescopeHealthState"
        )

        assert event_recorder.has_change_event_occurred(
            central_node.central_node, "telescopeHealthState", HealthState.OK
        )

    def set_subarray_health_state_as_OK(
        self, subarray_node, simulator_factory
    ):
        """_summary_

        Args:
            device (_type_): _description_
        """

        (
            csp_sa_sim,
            sdp_sa_sim,
            dish_master_1,
            dish_master_2,
        ) = get_device_simulators(simulator_factory)
        csp_sa_sim.SetDirectHealthState(HealthState.OK)
        sdp_sa_sim.SetDirectHealthState(HealthState.OK)
        dish_master_1.SetDirectHealthState(HealthState.OK)
        dish_master_2.SetDirectHealthState(HealthState.OK)

        assert subarray_node.subarray_node.healthState == HealthState.OK
