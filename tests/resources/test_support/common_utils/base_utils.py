"""
Simple class for checking device ObsState
"""
from tests.resources.test_support.helpers import resource


class DeviceUtils(object):
    """This class implement method for checking obsState of provided devices"""

    def __init__(self, **kwargs):
        """
        Args:
            kwargs (dict) - provide list of devices to check for obsState as
            value in dict
        """
        self.obs_state_device_names = kwargs.get("obs_state_device_names", [])

    def check_devices_obsState(self, obs_state) -> None:
        """
        Args:
            obs_state (str): ObsState to check for device
        """
        for device_name in self.obs_state_device_names:
            resource(device_name).assert_attribute("obsState").equals(
                obs_state
            )
