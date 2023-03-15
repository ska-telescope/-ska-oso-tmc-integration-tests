"""Base Utils class 
"""
from tests.resources.test_support.helpers import resource

class BaseTestUtils(object):
    
    def __init__(self, **kwargs):
        """
        """
        self.obs_state_device_names = kwargs.get("obs_state_device_names", [])

    def check_going_out_of_obsState(self, obs_state):
        """
        Args:
            obs_state (str): ObsState to check for device
            device_names (list): list of devices to check for obsState
        """
        # verify once for obstate = EMPTY
        for device_name in self.obs_state_device_names:
            resource(device_name).assert_attribute("obsState").equals(obs_state)
