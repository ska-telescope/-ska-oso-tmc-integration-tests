import logging
import queue
from collections import Counter
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pytest
from ska_control_model import ObsState
from ska_ser_logging import configure_logging
from ska_tango_testing.mock.tango import MockTangoEventCallbackGroup
from tango import EventType

from tests.resources.test_harness.subarray_node import SubarrayNodeWrapper

configure_logging(logging.DEBUG)
LOGGER = logging.getLogger(__name__)


@pytest.fixture
def constants():
    """Fixture for storing constants used in tests"""
    project_root = Path(__file__).absolute().parents[3]
    return {
        "PROJECT_ROOT": project_root,
        "DATA_DIR": project_root / "tests/integration/data/",
        "SCRIPTS_DIR": project_root / "tests/integration/data/scripts/",
    }


@dataclass
class EventsSummary:
    obsstate_counts: Counter[ObsState, int]
    """Counts how many times the device went through each obsState"""

    final_obsstate: Optional[ObsState]
    """Final device obsState at the end of the test"""

    def __init__(self, events: MockTangoEventCallbackGroup):
        """
        Create an EventsSummary from an ska-tango-testing MockTangoEventCallbackGroup.
        """
        self.obsstate_counts = Counter[ObsState, int]()
        self._summarise(events)

    def _summarise(self, events: MockTangoEventCallbackGroup):
        # TODO: write a consumer that will generate the desired events summary without inspecting private attrs
        q: queue.SimpleQueue = events["obsState"]._callable._call_queue
        final_obsstate = None
        while not q.empty():
            try:
                _, event_data, _ = q.get_nowait()
                # More brittle attribute access, although Tango EventData structure should be almost static
                event_value = event_data[0].attr_value.value
                obsstate = ObsState(event_value)
                self.obsstate_counts[obsstate] += 1
                final_obsstate = obsstate
            except queue.Empty:
                pass
        self.final_obsstate = final_obsstate


@contextmanager
def event_recorder(san: SubarrayNodeWrapper):
    change_event_callbacks = MockTangoEventCallbackGroup("obsState")
    san_proxy = san.subarray_node
    sid = san_proxy.subscribe_event(
        "obsState",
        EventType.CHANGE_EVENT,
        change_event_callbacks["obsState"],
    )
    yield change_event_callbacks
    san_proxy.unsubscribe_event(sid)
