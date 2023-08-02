import pytest
from ska_tango_base.control_model import HealthState

from tests.resources.test_harness.helpers import get_master_device_simulators


class TestTelescopeHealthState(object):
    """This class implement test cases to verify telescopeHealthState
    of CentralNode"""

    @pytest.mark.parametrize(
        "csp_master_health_state, sdp_master_health_state, \
        dish_master1_health_state, dish_master2_health_state",
        [
            (
                HealthState.OK,
                HealthState.FAILED,
                HealthState.OK,
                HealthState.OK,
            ),
            (
                HealthState.FAILED,
                HealthState.OK,
                HealthState.OK,
                HealthState.OK,
            ),
            (
                HealthState.OK,
                HealthState.OK,
                HealthState.FAILED,
                HealthState.OK,
            ),
            (
                HealthState.OK,
                HealthState.OK,
                HealthState.OK,
                HealthState.FAILED,
            ),
        ],
    )
    @pytest.mark.SKA_mid
    def test_telescope_health_state_failed(
        self,
        central_node,
        simulator_factory,
        event_recorder,
        csp_master_health_state,
        sdp_master_health_state,
        dish_master1_health_state,
        dish_master2_health_state,
    ):
        (
            csp_master_sim,
            sdp_master_sim,
            dish_master_1,
            dish_master_2,
        ) = get_master_device_simulators(simulator_factory)
        csp_master_sim.SetDirectHealthState(csp_master_health_state)
        sdp_master_sim.SetDirectHealthState(sdp_master_health_state)
        dish_master_1.SetDirectHealthState(dish_master1_health_state)
        dish_master_2.SetDirectHealthState(dish_master2_health_state)

        event_recorder.subscribe_event(
            central_node.central_node, "telescopeHealthState"
        )

        assert event_recorder.has_change_event_occurred(
            central_node.central_node,
            "telescopeHealthState",
            HealthState.FAILED,
        )

    @pytest.mark.skip(reason="Requires new SubarrayNode image version")
    @pytest.mark.SKA_mid
    def test_telescope_state_ok(
        self, central_node, subarray_node, event_recorder
    ):
        event_recorder.subscribe_event(
            central_node.central_node, "telescopeHealthState"
        )

        assert subarray_node.subarray_node.healthState == HealthState.OK
        assert event_recorder.has_change_event_occurred(
            central_node.central_node, "telescopeHealthState", HealthState.OK
        )
        assert central_node.central_node.telescopeHealthState == HealthState.OK

    @pytest.mark.parametrize(
        "csp_master_health_state, sdp_master_health_state, \
        dish_master1_health_state, dish_master2_health_state",
        [
            (
                HealthState.OK,
                HealthState.DEGRADED,
                HealthState.OK,
                HealthState.OK,
            ),
            (
                HealthState.DEGRADED,
                HealthState.OK,
                HealthState.OK,
                HealthState.OK,
            ),
            (
                HealthState.OK,
                HealthState.OK,
                HealthState.DEGRADED,
                HealthState.OK,
            ),
            (
                HealthState.OK,
                HealthState.OK,
                HealthState.OK,
                HealthState.DEGRADED,
            ),
        ],
    )
    @pytest.mark.SKA_mid
    def test_telescope_health_state_degraded(
        self,
        central_node,
        simulator_factory,
        event_recorder,
        csp_master_health_state,
        sdp_master_health_state,
        dish_master1_health_state,
        dish_master2_health_state,
    ):
        (
            csp_master_sim,
            sdp_master_sim,
            dish_master_1,
            dish_master_2,
        ) = get_master_device_simulators(simulator_factory)
        csp_master_sim.SetDirectHealthState(csp_master_health_state)
        sdp_master_sim.SetDirectHealthState(sdp_master_health_state)
        dish_master_1.SetDirectHealthState(dish_master1_health_state)
        dish_master_2.SetDirectHealthState(dish_master2_health_state)

        event_recorder.subscribe_event(
            central_node.central_node, "telescopeHealthState"
        )

        assert event_recorder.has_change_event_occurred(
            central_node.central_node,
            "telescopeHealthState",
            HealthState.DEGRADED,
        )
