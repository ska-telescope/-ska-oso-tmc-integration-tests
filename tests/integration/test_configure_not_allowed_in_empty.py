import pytest
from tests.resources.test_support.controls import subarray_obs_state_is_empty
import tests.resources.test_support.tmc_helpers as tmc
from tests.conftest import LOGGER
from tests.resources.test_support.helpers import resource
from tango import DeviceProxy
from tests.resources.test_support.constant import (
tmc_subarraynode1
)

configure_resources_file = "command_Configure.json" 

@pytest.mark.skip
@pytest.mark.SKA_mid
def test_configure_not_allowed_in_empty():   
    fixture = {}
    fixture["state"] = "Unknown"

    # Given a SubarrayNode in EMPTY observation state
    """Verify Subarray is in EMPTY state"""
    assert subarray_obs_state_is_empty()
    LOGGER.info("Subarray is in EMPTY state")

    """Invoke Configure() Command on TMC"""
    LOGGER.info("Invoking Configure command on TMC CentralNode")
    resource(tmc_subarraynode1).assert_attribute("obsState").equals(
        "EMPTY"
    )
    configure_input = tmc.get_input_str(configure_resources_file)            
    subarray_node = DeviceProxy(tmc_subarraynode1)
    with pytest.raises(Exception) as info:
        # When CONFIGURE command invoked
        subarray_node.Configure(configure_input)
    # Then it fails with Command not Allowed error
    assert "Configure command not permitted in observation state EMPTY" in str(info.value)
    # And TMC remains in EMPTY observation state
    assert subarray_obs_state_is_empty()