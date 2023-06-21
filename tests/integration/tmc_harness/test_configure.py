import pytest
from tests.resources.test_harness.helpers import check_state, check_obs_state
from tests.resources.test_support.tmc_helpers import tear_down

@pytest.mark.hope
@pytest.mark.SKA_Mid
def test_configure(subarray_node, json_factory):
   """
   Test module to verify Configure command, obsState transitions from IDLE to READY
   """
   release_json = json_factory("command_ReleaseResources")
   configure_json = json_factory("command_Configure")

   check_state(state = "ON")
#    if not check_obs_state(obs_state = "IDLE"):
#       subarray_node.force_obs_state(obs_state = "EMPTY", input = assign_json)

   check_obs_state(obs_state="IDLE")

   subarray_node.invoke_configure(configure_json)

   check_obs_state(obs_state="READY")

   #tear_down(release_json)


