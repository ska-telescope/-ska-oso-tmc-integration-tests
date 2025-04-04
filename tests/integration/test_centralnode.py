"""
Contains code for testing OSO's TMC SubArrayNode simulator in a Tango context.
"""

import json

import pytest
import tango
from ska_control_model import ObsState

from ska_oso_tmcsim import get_centralnode_trl, get_subarraynode_trl
from ska_oso_tmcsim.subarraynode import MethodCall

from .. import LOW_DOMAIN, MID_DOMAIN


class TestCentralNode:  # pylint: disable=too-few-public-methods
    """
    Tests the behaviour of the CentralNode simulator in a tango environment
    """

    @pytest.mark.parametrize("domain", [MID_DOMAIN, LOW_DOMAIN])
    def test_assign_resources_reaches_subarray(self, domain):
        """
        This is mainly a sanity check that the CentralNode device can be reached by tango
        and it is correctly communicating with the Sub-Array device.
        """
        # Arrange a test harness with a CentralNode and one Subarray
        centralnode_trl = get_centralnode_trl(domain)
        subarraynode_trl = get_subarraynode_trl(domain, 1)
        central_node_device = tango.DeviceProxy(centralnode_trl)
        subarray_device = tango.DeviceProxy(subarraynode_trl)
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

        expected = MethodCall(
            command="ReleaseResources", args=['{"release_all": true}']
        )
        assert history[1]["command"] == "ReleaseResources"
        assert MethodCall.model_validate(history[1]) == expected
        assert subarray_device.ObsState == ObsState.EMPTY
