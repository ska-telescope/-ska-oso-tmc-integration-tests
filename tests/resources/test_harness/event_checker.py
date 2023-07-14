"""Implement Event checker class which can be used to validate events
"""
from typing import Any

from ska_tango_testing.mock.tango.event_callback import (
    MockTangoEventCallbackGroup,
)
from tango import EventType


class AttributeNotSubscribed(Exception):
    # Raise this exception when attribute is not subscribed
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class EventChecker(object):
    """Implement method required for validating events"""

    def __init__(self):
        """Initialize events data"""
        self.subscribed_events = {}
        self.subscribed_devices = []

    def subscribe_event(
        self, device: Any, attribute_name: str, timeout: float = 50.0
    ):
        """Subscribe for change event for given attribute
        Args:
            device: Tango Device Proxy Object
            attribute_name (str): Name of the attribute
            timeout
        """
        obs_state_change_event_callback = MockTangoEventCallbackGroup(
            attribute_name,
            timeout=timeout,
        )
        event_id = device.subscribe_event(
            attribute_name,
            EventType.CHANGE_EVENT,
            obs_state_change_event_callback[attribute_name],
        )
        self.subscribed_devices.append((device, event_id))

        if attribute_name not in self.subscribed_events:
            self.subscribed_events[
                attribute_name
            ] = obs_state_change_event_callback

    def is_change_event_occurred(
        self, attribute_name: str, attribute_value: Any, lookahead: int = 5
    ) -> bool:
        """Validate Change Event occurred for provided attribute
        Args:
            attribute_name (str): Name of the attribute
            attribute_value : Value of attribute
        Returns:
            bool: Change Event occurred True or False
        """
        change_event_callback = self.subscribed_events.get(
            attribute_name, None
        )
        if change_event_callback:
            return change_event_callback[attribute_name].assert_change_event(
                attribute_value, lookahead=lookahead
            )

        raise AttributeNotSubscribed(
            f"Attribute {attribute_name} is not subscribed"
        )

    def clear_events(self):
        """Clear Subscribed Events"""
        for device, event_id in self.subscribed_devices:
            try:
                device.unsubscribe_event(event_id)
            except KeyError:
                # If event id is not subscribed then Key Error is raised
                pass
        self.subscribed_devices = []
        self.subscribed_events = {}
