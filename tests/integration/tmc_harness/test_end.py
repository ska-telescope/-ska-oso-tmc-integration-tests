import pytest

from tests.resources.test_harness.helpers import check_subarray_obs_state


@pytest.mark.end
@pytest.mark.SKA_mid
def test_end(subarray_node):
    """
    Test module to verify End command, obsState transitions from
    READY TO IDLE
    """

    if subarray_node.state != "ON":
        subarray_node.move_to_on()

    if subarray_node.obs_state != "READY":
        subarray_node.force_change_obs_state("READY")

    # assert check_obs_state(obs_state="READY")

    subarray_node.end_observation()

    check_subarray_obs_state(obs_state="IDLE")

    # tear_down(release_json)
