import pytest

from tests.resources.test_harness.helpers import (
    check_obs_state,
    check_subarray_state,
)
from tests.resources.test_support.tmc_helpers import tear_down


@pytest.mark.hope
@pytest.mark.SKA_Mid
def test_configure(subarray_node, json_factory):
    """
    Test module to verify Configure command, obsState transitions from IDLE to READY
    """
    release_json = json_factory("command_ReleaseResources")
    configure_json = json_factory("command_Configure")

    assert check_subarray_state(state="ON")

    if not check_obs_state(obs_state="IDLE"):
        subarray_node.force_change_obs_state("IDLE")

    assert check_obs_state(obs_state="IDLE")

    subarray_node.invoke_configure(configure_json)

    check_obs_state(obs_state="READY")

    # tear_down(release_json)
