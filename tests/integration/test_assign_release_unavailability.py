import pytest
from tango import DeviceProxy

import tests.resources.test_support.tmc_helpers as tmc
from tests.conftest import LOGGER
from tests.resources.test_support.constant import (
    DEVICE_HEALTH_STATE_OK_INFO,
    centralnode,
    tmc_subarraynode1,
)
from tests.resources.test_support.controls import (
    subarray_obs_state_is_empty,
    subarray_obs_state_is_idle,
    telescope_is_in_on_state,
    telescope_is_in_standby_state,
)
from tests.resources.test_support.helpers import resource
from tests.resources.test_support.exception import CommandNotAllowed
from tests.resources.test_support.sync_decorators import sync_assign_resources
from tests.resources.test_support.telescope_controls import (
    BaseTelescopeControl,
)
from tests.resources.test_support.tmc_helpers import tear_down

@pytest.mark.skip
@pytest.mark.SKA_mid
def test_assign_release(json_factory):
    """AssignResources and ReleaseResources is executed."""
    assign_json = json_factory("command_AssignResources")
    release_json = json_factory("command_ReleaseResources")
    try:
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

        with pytest.raises(CommandNotAllowed):
            subarray_node = DeviceProxy(tmc_subarraynode1)
            value = subarray_node.read_attribute("isSubarrayAvailable").value
            LOGGER.info(f"Attribute value::{value}")
            ret_code, message = subarray_node.AssignResources(assign_json)

        LOGGER.info(f"resultcode::{ret_code}")

        LOGGER.info("AssignResources command is invoked successfully")

    except Exception as e:
        LOGGER.info(f"Exception raise:{e}")



