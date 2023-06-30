"""Implement Class related to mock device
"""
from tango import DeviceProxy

from tests.resources.test_harness.constant import csp_subarray1, sdp_subarray1
from tests.resources.test_harness.utils.enums import MockDeviceType


class MockFactory(object):
    """This Mock factory used to implement method for creating
    Tango mock object
    """

    def create_mock_device(
        self, device_type, obs_state_transition_duration=None
    ):
        """This method create mock object based on mock type provided
        Args:
            device_type (str): Device type for which Mock need to be created
            obs_state_transition_duration (int): Obs State transition
            duration so device will change it's obs state after specified
            duration
        Returns:
            mock_device_proxy: Device Proxy of mock device
        """
        if device_type == MockDeviceType.SDP_DEVICE:
            mock_device = DeviceProxy(sdp_subarray1)
        elif device_type == MockDeviceType.CSP_DEVICE:
            mock_device = DeviceProxy(csp_subarray1)

        if obs_state_transition_duration:
            mock_device.setDelay(obs_state_transition_duration)

        return mock_device
