# TODO: WIP
# import pytest

# from tests.resources.test_harness.helpers import check_obs_state, check_state
# from tests.resources.test_support.tmc_helpers import tear_down


# @pytest.mark.hope
# @pytest.mark.SKA_Mid
# def test_assign_resources(central_node, json_factory):
#     """
#     Test module to verify AssignResources command, obsState transitions from EMPTY to IDLE
#     """
#     assign_json = json_factory("command_AssignResources")
#     release_json = json_factory("command_ReleaseResources")

#     check_state(state="OFF")
#     if not check_obs_state(obs_state="EMPTY"):
#         central_node.force_obs_state(obs_state="EMPTY", input=assign_json)

#     central_node.invoke_assign_resources(assign_json)
#     # change_obs_state()

#     check_obs_state(obs_state="IDLE")

#     tear_down(release_json)
