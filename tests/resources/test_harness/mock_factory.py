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

    def get_or_create_mock_device(self, device_type, mock_number=1):
        """This method create or get mock object based on device type provided
        Args:
            device_type (str): Device type for which Mock need to be created
            mock_number (int): Mock number device proxy object to return.
            Default return 1st Mock device
        Returns:
            mock_device_proxy: Device Proxy of mock device
        """
        if device_type in self._mock_dev:
            LOGGER.info(f"Found existing mock devcie for {device_type}")
            mock_device = self._mock_dev[device_type][mock_number]
        else:
            mock_fqdn_list = MOCK_DEVICE_FQDN_DICT.get(device_type)
            LOGGER.info(f"Initializing mock device for {mock_fqdn_list}")
            self._mock_dev[device_type] = {}
            for index, mock_fqdn in enumerate(sorted(mock_fqdn_list), start=1):
                device = DeviceProxy(mock_fqdn)
                self._mock_dev[device_type][index] = device
            mock_device = self._mock_dev[device_type][mock_number]

        return mock_device
