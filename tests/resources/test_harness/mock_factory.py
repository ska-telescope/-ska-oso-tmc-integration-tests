"""Implement Class related to mock device
"""
import logging

from tango import DeviceProxy

from tests.resources.test_harness.constant import MOCK_DEVICE_FQDN_DICT

LOGGER = logging.getLogger(__name__)


class MockFactory(object):
    """This Mock factory used to implement method for creating
    Tango mock object
    """

    def __init__(self):
        """Initialize mock object dict"""
        self._mock_dev = {}

    def get_or_create_mock_device(
        self, device_type, obs_state_transition_duration=None
    ):
        """This method create or get mock object based on device type provided
        Args:
            device_type (str): Device type for which Mock need to be created
            obs_state_transition_duration (int): Obs State transition
            duration so device will change it's obs state after specified
            duration
        Returns:
            mock_device_proxy: Device Proxy of mock device
        """
        if device_type in self._mock_dev:
            LOGGER.info(f"Found existing mock devcie for {device_type}")
            mock_device = self._mock_dev[device_type]
        else:
            mock_fqdn = MOCK_DEVICE_FQDN_DICT.get(device_type)
            LOGGER.info(f"Initializing mock device for {mock_fqdn}")
            mock_device = DeviceProxy(mock_fqdn)
            self._mock_dev[device_type] = mock_device

        return mock_device
