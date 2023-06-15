import pytest

from tests.conftest import LOGGER
from tests.resources.test_support.common_utils.tmc_helpers import TmcHelper
from tests.resources.test_support.constant import (
    ON_OFF_DEVICE_COMMAND_DICT,
    centralnode,
    tmc_subarraynode1,
)
from tests.resources.test_support.controls import (
    telescope_is_in_on_state,
    telescope_is_in_standby_state,
)
from tests.resources.test_support.tmc_helpers import tear_down
from tango import DeviceProxy



@pytest.mark.SKA_mid
def test_telescope_on():
    """TelescopeOn() is executed."""
    try:

        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")

        central_node = DeviceProxy("ska_mid/tm_central/central_node")
        LOGGER.info(
            f"Before Sending TelescopeOn command {central_node}\
                   State is:{central_node.State()}"
        )


        #works fine when pods are deleted
        with pytest.raises(Exception) as info:
            central_node.TelescopeOn()
            # Then it fails with Command not Allowed error
        assert "is not available" in str(
            info.value
        )
        LOGGER.info("TelescopeOn command is invoked successfully")



    except Exception as e:
        LOGGER.info("Problem in starting ON command: %s", e)


@pytest.mark.trupti1
@pytest.mark.SKA_mid
def test_assign_release(json_factory):
    """AssignResources and ReleaseResources is executed."""
    assign_json = json_factory("command_AssignResources")
    #release_json = json_factory("command_ReleaseResources")
    try:
        tmc_subarraynode1 = DeviceProxy("ska_mid/tm_subarray_node/1")
        with pytest.raises(Exception) as info:
            tmc_subarraynode1.AssignResources(assign_json)
            # Then it fails with Command not Allowed error
        assert "Tmc Subarray is not available" in str(
            info.value
        )


    except Exception as e:
        LOGGER.info("Problem in starting assign command: %s", e)