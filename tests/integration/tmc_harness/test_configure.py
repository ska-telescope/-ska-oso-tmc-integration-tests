import pytest

from tests.resources.test_harness.helpers import check_subarray_obs_state


@pytest.mark.hope
@pytest.mark.SKA_mid
def test_configure(subarray_node, json_factory):
    """
    Test module to verify Configure command, obsState transitions from
    IDLE to READY
    """
    configure_json = json_factory("command_Configure")

    if subarray_node.state != "ON":
        subarray_node.move_to_on()

    if subarray_node.obs_state != "IDLE":
        subarray_node.force_change_obs_state("IDLE")

    assert check_subarray_obs_state(obs_state="IDLE")

    subarray_node.configure_subarray(configure_json)

    check_subarray_obs_state(obs_state="READY")
