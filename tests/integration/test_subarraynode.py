"""
Contains code for testing OSO's TMC SubArrayNode simulator in a Tango context.
"""

import json
import operator

import pytest
import tango
from ska_control_model import ObsState

from ska_oso_tmcsim import get_subarraynode_trl
from ska_oso_tmcsim.subarraynode import MethodCall

from .. import LOW_DOMAIN, MID_DOMAIN


class TestSubarrayNode:  # pylint: disable=too-few-public-methods
    """
    Tests for the SubArrayNode simulator in tango environment.
    """

    @pytest.mark.parametrize("domain", [MID_DOMAIN, LOW_DOMAIN])
    @pytest.mark.parametrize(
        "initial_obsstate,method,args",
        [
            (ObsState.EMPTY, "AssignResources", ["{'foo': 'bar'}"]),
            (ObsState.IDLE, "Configure", ["{'foo': 'bar'}"]),
            (ObsState.READY, "Scan", ["{'foo': 'bar'}"]),
            (ObsState.READY, "End", []),
            (ObsState.IDLE, "Abort", []),
            (ObsState.ABORTED, "Restart", []),
        ],
    )
    def test_subarray_state_lifecycle(self, domain, initial_obsstate, method, args):
        """
        Tests that commands and arguments are recorded in the device history.
        """
        f = operator.methodcaller(method, *args)
        subarray_trl = get_subarraynode_trl(domain, 1)
        device = tango.DeviceProxy(subarray_trl)
        assert device.ObsState == initial_obsstate
        f(device)
        history = json.loads(device.History)

        expected = MethodCall(command=method, args=args)
        assert MethodCall.model_validate(history[0]) == expected

        # Clear the history after every test so that it is always the first
        # entry in the history that we check
        device.ClearHistory()
