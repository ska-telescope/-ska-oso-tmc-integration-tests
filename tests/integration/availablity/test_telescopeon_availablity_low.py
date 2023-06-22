import pytest
from tango import DeviceProxy

from tests.conftest import LOGGER
from tests.resources.test_support.constant_low import (
    centralnode,
    tmc_subarraynode1,
)

# These test case will pass only when any of the node is deleted explicitly
# Hence this test will be skipped on pipeline
# Sample command to delete is
# while true;
# do kubectl delete pod/subarraynode-02-0 -n ska-tmc-integration; sleep 3;
# done


# @pytest.mark.skip(reason="Manual deletion of pods is required ")
@pytest.mark.SKA_low11
def test_assign(json_factory):
    """AssignResources and ReleaseResources is executed."""

    assign_json = json_factory("command_assign_resource_low")
    central_node = DeviceProxy(centralnode)

    result, message = central_node.AssignResources(assign_json)
    assert "not available" in str(message)


# @pytest.mark.skip(reason="Manual deletion of pods is required ")
@pytest.mark.SKA_low11
def test_release(json_factory):
    """ReleaseResources is executed."""

    release_json = json_factory("command_release_resource_low")
    central_node = DeviceProxy(centralnode)

    result, message = central_node.ReleaseResources(release_json)

    assert "not available" in str(message)


# @pytest.mark.skip(reason="Manual deletion of pods is required ")
@pytest.mark.SKA_low11
def test_telescope_on():

    LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")

    central_node = DeviceProxy(centralnode)
    LOGGER.info(
        f"Before Sending TelescopeOn command {central_node}\
                   State is:{central_node.State()}"
    )

    # works fine when pods are deleted
    with pytest.raises(Exception) as info:
        central_node.TelescopeOn()
        # Then it fails with Command not Allowed error
    assert "not available" in str(info.value)
    LOGGER.info("TelescopeOn command is invoked successfully")


# @pytest.mark.skip(reason="Manual deletion of pods is required ")
@pytest.mark.SKA_low11
def test_assign_sn_entrypoint_low(json_factory):
    """AssignResources and ReleaseResources is executed."""
    assign_json = json_factory("command_assign_resource_low")

    tmcsubarraynode1 = DeviceProxy(tmc_subarraynode1)
    with pytest.raises(Exception) as info:
        tmcsubarraynode1.AssignResources(assign_json)
        # Then it fails with Command not Allowed error
    LOGGER.info(info)
    assert "Tmc Subarray is not available" in str(info.value)


# @pytest.mark.skip(reason="Manual deletion of pods is required ")
@pytest.mark.SKA_low11
def test_release_sn_entrypoint_low(json_factory):
    """AssignResources and ReleaseResources is executed."""

    tmcsubarraynode1 = DeviceProxy(tmc_subarraynode1)
    with pytest.raises(Exception) as info:
        tmcsubarraynode1.ReleaseAllResources()
        # Then it fails with Command not Allowed error
    assert "Tmc Subarray is not available" in str(info.value)
