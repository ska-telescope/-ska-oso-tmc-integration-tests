"""
Contains code for testing OSO's TMC SubArrayNode simulator in a Tango context.
"""

import json
import operator

import pytest
from ska_control_model import ObsState

from ska_oso_tmc_integration_tests.tmcsim.subarraynode import MethodCall
from ska_oso_tmc_integration_tests.tmcsim.testharness import TMCSimTestHarness

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
            (ObsState.IDLE, "ReleaseResources", ["{'foo': 'bar'}"]),
            (ObsState.READY, "Scan", ["{'foo': 'bar'}"]),
            (ObsState.READY, "Abort", []),
            (ObsState.READY, "End", []),
            (ObsState.ABORTED, "Restart", []),
        ],
    )
    def test_arguments_recorded(self, base_uri, initial_obsstate, method, args):
        """
        Tests that commands and arguments are recorded in the device history.
        """
        test_harness = TMCSimTestHarness(base_uri=base_uri)
        test_harness.add_subarray(1, initial_obsstate=initial_obsstate)

        with test_harness as ctx:
            f = operator.methodcaller(method, *args)
            device = ctx.get_device(f"{base_uri}/tm_subarray_node/1")
            f(device)
            history = json.loads(device.History)

        expected = MethodCall(command=method, args=args)
        assert MethodCall.model_validate(history[0]) == expected

    @pytest.mark.parametrize("base_uri", [MID_BASE_URI, LOW_BASE_URI])
    def test_history_cleared(self, base_uri):
        """
        Tests that the command history is cleared when ClearHistory is called.
        """
        test_harness = TMCSimTestHarness(base_uri=base_uri)
        test_harness.add_subarray(1, initial_obsstate=ObsState.IDLE)

        with test_harness as ctx:
            san = ctx.get_device(f"{base_uri}/tm_subarray_node/1")
            san.Configure("{'foo': 'bar'}")
            history = json.loads(san.History)
            assert len(history) > 0
            san.ClearHistory()
            history = json.loads(san.History)
            assert len(history) == 0

    def test_fault_can_be_injected(self, base_uri="ska-test"):
        """
        Tests that the SubarrayNode can be configured to go to a FAULT state for
        a given series of commands.
        """
        test_harness = TMCSimTestHarness(base_uri=base_uri)
        test_harness.add_subarray(1, initial_obsstate=ObsState.IDLE)

        with test_harness as ctx:
            san = ctx.get_device(f"{base_uri}/tm_subarray_node/1")
            # Set the device up so it will go to FAULT after moving
            # through a given sequence of states
            san.InjectFaultAfter("['IDLE', 'CONFIGURING', 'READY']")
            # Send a command which should move the device through the above states
            san.Configure("{'foo': 'bar'}")
            # Assert the state has gone to Fault
            assert san.obsState == ObsState.FAULT
