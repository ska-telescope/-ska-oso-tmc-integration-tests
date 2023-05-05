import time

from tests.conftest import LOGGER
from tests.resources.test_support.low.helpers import resource


class BaseTelescopeControl(object):
    """Base Telescope control class.
    Use this class to write method to check status of devices
    """

    def is_in_valid_state(self, device_state_info, state_str):
        """Validate device state is in desired state as per device state info
        Args:
            device_state_info (dict): device name and it's expected state info
        """
        state_result_list = []
        for device in device_state_info:
            state_list = device_state_info.get(device)
            device_state = resource(device).get(state_str)
            LOGGER.info(
                f"resource({device}).get('{state_str}') : {device_state}"
            )
            state_result_list.append(
                resource(device).get(state_str) in state_list
            )

        return all(state_result_list)
