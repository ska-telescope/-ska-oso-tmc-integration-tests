import pytest

from tests.conftest import LOGGER
from tango import DeviceProxy
#These test case will pass only when any of the node is deleted explicitly
#Hence this test will be skipped on pipeline
# Sample command to delete is
# while true; do kubectl delete pod/subarraynode-02-0 -n ska-tmc-integration; sleep 3; done
@pytest.mark.SKA_mid1
def test_telescope_on_mid():
    """TelescopeOn() is executed."""
    LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")

    central_node = DeviceProxy("ska_mid/tm_central/central_node")
    LOGGER.info(
        f"Before Sending TelescopeOn command {central_node}\
                       State is:{central_node.State()}"
    )

    # works fine when pods are deleted
    with pytest.raises(Exception) as info:
        central_node.TelescopeOn()
        # Then it fails with Command not Allowed error
    assert "not available" in str(
        info.value
    )
    LOGGER.info("TelescopeOn command is invoked successfully")



@pytest.mark.SKA_mid1
def test_assign_sn_entrypoint(json_factory):
    """AssignResources and ReleaseResources is executed."""
    assign_json = json_factory("command_AssignResources")

    tmc_subarraynode1 = DeviceProxy("ska_mid/tm_subarray_node/1")
    with pytest.raises(Exception) as info:
            tmc_subarraynode1.AssignResources(assign_json)
            # Then it fails with Command not Allowed error
    LOGGER.info(info)
    assert "Tmc Subarray is not available" in str(
            info.value
        )

@pytest.mark.SKA_mid1
def test_release_sn_entrypoint(json_factory):
        """AssignResources and ReleaseResources is executed."""


        tmc_subarraynode1 = DeviceProxy("ska_mid/tm_subarray_node/1")
        with pytest.raises(Exception) as info:
            tmc_subarraynode1.ReleaseAllResources()
            # Then it fails with Command not Allowed error
        assert "Tmc Subarray is not available" in str(
            info.value
        )

#Assign / Release for central node can be automated
#Rest of the command can not be automated.

@pytest.mark.SKA_mid1
def test_assign_mid(json_factory):
    """AssignResources and ReleaseResources is executed."""
    assign_json = json_factory("command_AssignResources")

    central_node = DeviceProxy("ska_mid/tm_central/central_node")
    result, message = central_node.AssignResources(assign_json)
            # Then it fails with Command not Allowed error
    assert "Subarray ska_mid/tm_subarray_node/1 is not available" in str(
            message
        )

@pytest.mark.SKA_mid1
def test_release_mid(json_factory):
    """AssignResources and ReleaseResources is executed."""

    release_json = json_factory("command_ReleaseResources")
    central_node = DeviceProxy("ska_mid/tm_central/central_node")
    result, message = central_node.ReleaseResources(release_json)

    assert "Subarray ska_mid/tm_subarray_node/1 is not available" in str(
            message
        )

@pytest.mark.SKA_low1
def test_assign(json_factory):
        """AssignResources and ReleaseResources is executed."""

        assign_json = json_factory("command_assign_resource_low")
        central_node = DeviceProxy("ska_low/tm_central/central_node")

        result, message = central_node.AssignResources(assign_json)
        assert "not available" in str(
                 message
                )


@pytest.mark.SKA_low1
def test_release(json_factory):
        """ ReleaseResources is executed."""

        release_json = json_factory("command_release_resource_low")
        central_node = DeviceProxy("ska_low/tm_central/central_node")

        result, message = central_node.ReleaseResources(release_json)

        assert "not available" in str(
            message
        )


@pytest.mark.SKA_low1
def test_telescope_on():
        # """TelescopeOn() is executed."""

        LOGGER.info("Invoking TelescopeOn command on TMC CentralNode")

        central_node = DeviceProxy("ska_low/tm_central/central_node")
        LOGGER.info(
            f"Before Sending TelescopeOn command {central_node}\
                   State is:{central_node.State()}"
        )


        #works fine when pods are deleted
        with pytest.raises(Exception) as info:
            central_node.TelescopeOn()
            # Then it fails with Command not Allowed error
        assert "not available" in str(
            info.value
        )
        LOGGER.info("TelescopeOn command is invoked successfully")


@pytest.mark.SKA_low1
def test_assign_sn_entrypoint_low(json_factory):
    """AssignResources and ReleaseResources is executed."""
    assign_json = json_factory("command_assign_resource_low")

    tmc_subarraynode1 = DeviceProxy("ska_low/tm_subarray_node/1")
    with pytest.raises(Exception) as info:
            tmc_subarraynode1.AssignResources(assign_json)
            # Then it fails with Command not Allowed error
    LOGGER.info(info)
    assert "Tmc Subarray is not available" in str(
            info.value
        )

@pytest.mark.SKA_low1
def test_release_sn_entrypoint_low(json_factory):
        """AssignResources and ReleaseResources is executed."""


        tmc_subarraynode1 = DeviceProxy("ska_low/tm_subarray_node/1")
        with pytest.raises(Exception) as info:
            tmc_subarraynode1.ReleaseAllResources()
            # Then it fails with Command not Allowed error
        assert "Tmc Subarray is not available" in str(
            info.value
        )