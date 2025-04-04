"""
Contains code for testing OSO's TMC SubArrayNode simulator in a Tango context.
"""

import json
import operator
from time import time

import pytest
from ska_control_model import ObsState

from ska_oso_tmcsim import get_subarraynode_trl
from ska_oso_tmcsim.subarraynode import MethodCall
from ska_oso_tmcsim.testharness import TMCSimTestHarness

from .. import LOW_DOMAIN, MID_DOMAIN


class TestSubarrayNode:  # pylint: disable=too-few-public-methods
    """
    Tests for the SubArrayNode simulator that are unrelated to the state
    model, which is tested separately in unit tests.
    """

    @pytest.mark.parametrize("domain", [MID_DOMAIN, LOW_DOMAIN])
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
    def test_arguments_recorded(self, domain, initial_obsstate, method, args):
        """
        Tests that commands and arguments are recorded in the device history.
        """
        test_harness = TMCSimTestHarness(domain=domain)
        test_harness.add_subarray(1, initial_obsstate=initial_obsstate)

        with test_harness as ctx:
            f = operator.methodcaller(method, *args)
            subarray_trl = get_subarraynode_trl(domain, 1)
            device = ctx.get_device(subarray_trl)
            f(device)
            history = json.loads(device.History)

        expected = MethodCall(command=method, args=args)
        assert MethodCall.model_validate(history[0]) == expected

    @pytest.mark.parametrize("domain", [MID_DOMAIN, LOW_DOMAIN])
    def test_history_cleared(self, domain):
        """
        Tests that the command history is cleared when ClearHistory is called.
        """
        test_harness = TMCSimTestHarness(domain=domain)
        test_harness.add_subarray(1, initial_obsstate=ObsState.IDLE)

        with test_harness as ctx:
            subarray_trl = get_subarraynode_trl(domain, 1)
            san = ctx.get_device(subarray_trl)
            san.Configure("{'foo': 'bar'}")
            history = json.loads(san.History)
            assert len(history) > 0
            san.ClearHistory()
            history = json.loads(san.History)
            assert len(history) == 0

    def test_fault_can_be_injected(self, domain="ska-test"):
        """
        Tests that the SubarrayNode can be configured to go to a FAULT state for
        a given series of commands.
        """
        test_harness = TMCSimTestHarness(domain=domain)
        test_harness.add_subarray(1, initial_obsstate=ObsState.IDLE)

        with test_harness as ctx:
            subarray_trl = get_subarraynode_trl(domain, 1)
            san = ctx.get_device(subarray_trl)
            # Set the device up so it will go to FAULT after moving
            # through a given sequence of states
            san.InjectFaultAfter("['IDLE', 'CONFIGURING', 'READY']")
            # Send a command which should move the device through the above states
            san.Configure("{'foo': 'bar'}")
            # Assert the state has gone to Fault
            assert san.obsState == ObsState.FAULT

    @pytest.mark.parametrize("command_str", ["Configure", "AssignResources"])
    def test_delay_can_be_injected(self, command_str):
        """
        Tests that the SubarrayNode can be configured to add delays to
        individual supported commands.
        """
        domain = "ska-test"
        test_harness = TMCSimTestHarness(domain=domain)
        test_harness.add_subarray(1, initial_obsstate=ObsState.IDLE)

        with test_harness as ctx:
            subarray_trl = get_subarraynode_trl(domain, 1)
            san = ctx.get_device(subarray_trl)
            delay_s = 0.1
            san_cmd = getattr(san, command_str)

            # First check the command is less than the delay before it has been injected
            start = time()
            san_cmd("{'foo': 'bar'}")
            end = time()
            assert (end - start) < delay_s

            # Inject the delay
            san.InjectDelay(json.dumps({command_str: delay_s}))

            # Check the command now takes longer than the delay
            start = time()
            san_cmd("{'foo': 'bar'}")
            end = time()
            assert (end - start) > delay_s
