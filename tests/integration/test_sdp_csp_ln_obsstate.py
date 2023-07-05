import pytest
from ska_tango_base.control_model import ObsState
from tango import DeviceProxy

import tests.resources.test_support.tmc_helpers as tmc
from tests.conftest import LOGGER
from tests.resources.test_support.constant import (
    centralnode,
    tmc_csp_subarray_leaf_node,
    tmc_sdp_subarray_leaf_node,
    tmc_subarraynode1,
)
from tests.resources.test_support.controls import (
    subarray_obs_state_is_empty,
    subarray_obs_state_is_idle,
    telescope_is_in_on_state,
    telescope_is_in_standby_state,
)
from tests.resources.test_support.helpers import resource
from tests.resources.test_support.sync_decorators import sync_assign_resources
from tests.resources.test_support.tmc_helpers import tear_down


@pytest.mark.SKA_mid
def test_assign_release(json_factory):
    """AssignResources and ReleaseResources is executed."""
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")
    try:
        tmc.check_devices()

        # Verify Telescope is Off/Standby
        assert telescope_is_in_standby_state()
        LOGGER.info("Staring up the Telescope")

        # Invoke TelescopeOn() command on TMC
        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")
        tmc.set_to_on()
        LOGGER.info("TelescopeOn command is invoked successfully")

        # Verify State transitions after TelescopeOn
        assert telescope_is_in_on_state()

        # Invoke AssignResources() Command on TMC
        LOGGER.info("Invoking AssignResources command on TMC CentralNode")

        @sync_assign_resources()
        def compose_sub():
            resource(tmc_subarraynode1).assert_attribute("State").equals("ON")
            resource(tmc_subarraynode1).assert_attribute("obsState").equals(
                "EMPTY"
            )
            resource(tmc_csp_subarray_leaf_node).assert_attribute(
                "cspSubarrayObsState"
            ).equals(ObsState.EMPTY)
            resource(tmc_sdp_subarray_leaf_node).assert_attribute(
                "sdpSubarrayObsState"
            ).equals("EMPTY")
            central_node = DeviceProxy(centralnode)
            tmc.check_devices()
            central_node.AssignResources(assign_json)
            LOGGER.info("Invoked AssignResources on CentralNode")

        compose_sub()

        LOGGER.info("AssignResources command is invoked successfully")
        # Verfiy ObsState of csp and sdp subarray leafnode
        resource(tmc_csp_subarray_leaf_node).assert_attribute(
            "cspSubarrayObsState"
        ).equals(ObsState.IDLE)
        resource(tmc_sdp_subarray_leaf_node).assert_attribute(
            "sdpSubarrayObsState"
        ).equals("IDLE")
        # Verify ObsState is Idle
        assert subarray_obs_state_is_idle()

        # Invoke ReleaseResources() command on TMC
        tmc.invoke_releaseResources(release_json)

        assert subarray_obs_state_is_empty()

        # Invoke TelescopeStandby() command on TMC
        tmc.set_to_standby()

        # Verify State transitions after TelescopeStandby
        assert telescope_is_in_standby_state()

        LOGGER.info("Tests complete.")

    except Exception:
        tear_down(release_json)
