"""
Contains code for testing OSO's TMC SubArrayNode simulator in a Tango context.
"""

import json
import operator
import tango

import pytest
from ska_control_model import ObsState

from ska_oso_tmc_integration_tests.tmcsim.subarraynode import MethodCall

from . import LOW_BASE_URI, MID_BASE_URI


class TestSubarrayNode:  # pylint: disable=too-few-public-methods
    """
    Tests for the SubArrayNode simulator that are unrelated to the state
    model, which is tested separately in unit tests.
    """

    @pytest.mark.parametrize("base_uri", [MID_BASE_URI, LOW_BASE_URI])
    @pytest.mark.parametrize(
        "initial_obsstate,method,args",
        [
            (ObsState.EMPTY, "AssignResources", ["{'foo': 'bar'}"]),
            (ObsState.IDLE, "Configure", ["{'foo': 'bar'}"]),
            (ObsState.READY, "Scan", ["{'foo': 'bar'}"]),
            (ObsState.READY, "End", []),
            (ObsState.IDLE, "Abort", []),
            (ObsState.ABORTED, "Restart", [])
        ],
    )
    def test_subarray_state_lifecycle(self, base_uri, initial_obsstate, method, args):
        """
        Tests that commands and arguments are recorded in the device history.
        """
        f = operator.methodcaller(method, *args)
        device = tango.DeviceProxy(f"{base_uri}/tm_subarray_node/1")
        assert device.ObsState == initial_obsstate
        f(device)
        history = json.loads(device.History)

        expected = MethodCall(command=method, args=args)
        assert MethodCall.model_validate(history[0]) == expected

        # Clear the history after every test so that it is always the first
        # entry in the history that we check
        device.ClearHistory()
