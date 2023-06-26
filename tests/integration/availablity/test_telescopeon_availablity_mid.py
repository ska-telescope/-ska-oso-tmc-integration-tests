import pytest
from tango import DeviceProxy

from tests.resources.test_support.constant import (
    centralnode,
    tmc_subarraynode1,
)


# These test case will pass only when any of the node is deleted explicitly
# Hence this test will be skipped on pipeline
# Sample command to delete is
# while true;
# do kubectl delete pod/subarraynode-02-0 -n ska-tmc-integration; sleep 3;
# done
@pytest.mark.xfail(reason="Manual deletion of pods is required")
@pytest.mark.SKA_mid
def test_telescope_on_mid():
    """TelescopeOn() is executed while pods are deleted."""

    central_node = DeviceProxy(centralnode)

    with pytest.raises(Exception) as info:
        central_node.TelescopeOn()

    assert "not available" in str(info.value)


@pytest.mark.xfail(reason="Manual deletion of pods is required")
@pytest.mark.SKA_mid
def test_assign_sn_entrypoint(json_factory):
    """AssignResources is executed while pods are deleted."""
    assign_json = json_factory("command_AssignResources")

    tmcsubarraynode1 = DeviceProxy(tmc_subarraynode1)
    with pytest.raises(Exception) as info:
        tmcsubarraynode1.AssignResources(assign_json)

    assert "Tmc Subarray is not available" in str(info.value)


@pytest.mark.xfail(reason="Manual deletion of pods is required")
@pytest.mark.SKA_mid
def test_release_sn_entrypoint(json_factory):
    """ReleaseResources is executed while pods are deleted."""

    tmcsubarraynode1 = DeviceProxy(tmc_subarraynode1)
    with pytest.raises(Exception) as info:
        tmcsubarraynode1.ReleaseAllResources()

    assert "Tmc Subarray is not available" in str(info.value)


# Assign / Release for central node can be automated
# Rest of the command can not be automated.


@pytest.mark.xfail(reason="Manual deletion of pods is required")
@pytest.mark.SKA_mid
def test_assign_mid(json_factory):
    """AssignResources is executed while pods are deleted."""
    assign_json = json_factory("command_AssignResources")

    central_node = DeviceProxy(centralnode)
    result, message = central_node.AssignResources(assign_json)

    assert "Subarray ska_mid/tm_subarray_node/1 is not available" in str(
        message
    )


@pytest.mark.xfail(reason="Manual deletion of pods is required")
@pytest.mark.SKA_mid
def test_release_mid(json_factory):
    """ReleaseResources is executed while pods are deleted."""

    release_json = json_factory("command_ReleaseResources")
    central_node = DeviceProxy(centralnode)
    result, message = central_node.ReleaseResources(release_json)

    assert "Subarray ska_mid/tm_subarray_node/1 is not available" in str(
        message
    )
