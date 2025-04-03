"""
This module contains code related to running the OSO simulators in a test Tango
context.
"""

import logging

from ska_control_model import ObsState
from ska_ser_logging import configure_logging
from ska_tango_testing.harness import TangoTestHarness

from ska_oso_tmcsim import (
    CentralNode,
    SubArrayNode,
    construct_central_node_trl,
    construct_subarraynode_trl,
)

configure_logging(logging.DEBUG)
LOGGER = logging.getLogger(__name__)


class TMCSimTestHarness:
    """
    TMCSimTestHarness is an integration test harness for OSO's TMC Simulator.

    TMCSimTestHarness can populate a Tango test context with an OSO
    CentralNode simulator and an OSO SubArrayNode simulator to allow testing
    of the simulators and code that requires access to simulated TMC.
    """

    def __init__(self, base_uri="mid-tmc"):
        """
        Create a new TMCSimTestHarness.
        """
        self._tango_test_harness = TangoTestHarness()
        self._base_uri = base_uri

    def add_central_node(self):
        """
        Make CentralNode available within the test context.
        """
        self._tango_test_harness.add_device(
            device_name=construct_central_node_trl(self._base_uri),
            device_class=CentralNode,
            base_uri=self._base_uri,
        )

    def add_subarray(
        self, subarray_id: int, initial_obsstate: ObsState = ObsState.EMPTY
    ):
        """
        Add a subarray to the test harness.

        The subarray obsState will be set to the default obsState of EMPTY
        unless overridden.
        """
        trl = construct_subarraynode_trl(self._base_uri, subarray_id)
        device_props = dict(initial_obsstate=initial_obsstate.value)
        self._tango_test_harness.add_device(
            device_name=trl, device_class=SubArrayNode, **device_props
        )

    def __enter__(self):
        return self._tango_test_harness.__enter__()

    def __exit__(self, exc_type, exception, trace):
        return self._tango_test_harness.__exit__(exc_type, exception, trace)
