import pytest
from ska_tango_base.control_model import ObsState

from tests.conftest import LOGGER
from tests.resources.test_support.common_utils.tmc_helpers import TmcHelper
from tests.resources.test_support.constant_low import (
    DEVICE_OBS_STATE_EMPTY_INFO,
    DEVICE_OBS_STATE_IDLE_INFO,
    DEVICE_STATE_ON_INFO,
    DEVICE_STATE_STANDBY_INFO,
    ON_OFF_DEVICE_COMMAND_DICT,
    centralnode,
    tmc_csp_subarray_leaf_node,
    tmc_sdp_subarray_leaf_node,
    tmc_subarraynode1,
)
from tests.resources.test_support.helpers import resource
from tests.resources.test_support.low.telescope_controls_low import (
    TelescopeControlLow,
)
from tests.resources.test_support.tmc_helpers import tear_down


@pytest.mark.SKA_low
def test_csp_sdp_ln_obstate_low(json_factory, change_event_callbacks):
    """Verify timeout exception raised when csp set to defective."""
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")
    try:
        telescope_control = TelescopeControlLow()
        tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)

        # Verify Telescope is Off/Standby
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_STANDBY_INFO, "State"
        )

        # Invoke TelescopeOn() command on TMC
        tmc_helper.set_to_on(**ON_OFF_DEVICE_COMMAND_DICT)

        # Verify State transitions after TelescopeOn
        assert telescope_control.is_in_valid_state(
            DEVICE_STATE_ON_INFO, "State"
        )

        # Verify the CspSubarrayLeafNode and SdpSubarrayLeafNode obsState

        resource(tmc_csp_subarray_leaf_node).assert_attribute(
            "cspSubarrayObsState"
        ).equals(ObsState.EMPTY)
        resource(tmc_sdp_subarray_leaf_node).assert_attribute(
            "sdpSubarrayObsState"
        ).equals("EMPTY")

        # Invoke AssignResources() Command on TMC
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")

        tmc_helper.compose_sub(assign_json, **ON_OFF_DEVICE_COMMAND_DICT)

        # Verify ObsState is IDLE
        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_IDLE_INFO, "obsState"
        )
        # Verify the CspSubarrayLeafNode and SdpSubarrayLeafNode obsState

        resource(tmc_csp_subarray_leaf_node).assert_attribute(
            "cspSubarrayObsState"
        ).equals(ObsState.IDLE)
        resource(tmc_sdp_subarray_leaf_node).assert_attribute(
            "sdpSubarrayObsState"
        ).equals("IDLE")

        tmc_helper.invoke_releaseResources(
            release_json, **ON_OFF_DEVICE_COMMAND_DICT
        )

        assert telescope_control.is_in_valid_state(
            DEVICE_OBS_STATE_EMPTY_INFO, "obsState"
        )
        # Do not raise exception
        tear_down(release_json, raise_exception=False)

    except Exception as e:
        LOGGER.info(f"Exception occurred {e}")
        tear_down(release_json)
