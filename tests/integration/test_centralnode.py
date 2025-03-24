"""
Contains code for testing OSO's TMC SubArrayNode simulator in a Tango context.
"""

import json

import pytest
import tango
from ska_control_model import ObsState

from ska_oso_tmc_integration_tests.tmcsim.subarraynode import MethodCall

from . import LOW_BASE_URI, MID_BASE_URI


class TestCentralNode:  # pylint: disable=too-few-public-methods
    """
    Tests the behaviour of the CentralNode simulator
    """

    @pytest.mark.parametrize("base_uri", [MID_BASE_URI, LOW_BASE_URI])
    def test_assign_resources_reaches_subarray(self, base_uri):
        """
        This is mainly a sanity check that passing the base_uri property to the
        CentralNode works and this is then used when communicating with the subarray.

        It is kind of a test of the TMCSimTestHarness too, in that it checks that the
        base_uri from the constructor is passed properly during add_central_node()
        """
        # Arrange a test harness with a CentralNode and one Subarray
        central_node_device = tango.DeviceProxy(f"{base_uri}/tm_central/central_node")
        subarray_device = tango.DeviceProxy(f"{base_uri}/tm_subarray_node/1")
        assert subarray_device.ObsState == ObsState.EMPTY

        # Act: send a command to CentralNode
        central_node_device.AssignResources("{'foo': 'bar'}")

        # Assert the command was sent to the subarray
        history = json.loads(subarray_device.History)

        expected = MethodCall(command="AssignResources", args=["{'foo': 'bar'}"])
        assert MethodCall.model_validate(history[0]) == expected
        assert subarray_device.ObsState == ObsState.IDLE
        central_node_device.ReleaseResources('{"release_all": true}')

        # Assert the command was sent to the subarray
        history = json.loads(subarray_device.History)

        expected = MethodCall(command="ReleaseResources", args=['{"release_all": true}'])
        assert history[1]['command'] == "ReleaseResources"
        assert MethodCall.model_validate(history[1]) == expected
        assert subarray_device.ObsState == ObsState.EMPTY
