import time

from tests.conftest import LOGGER
from tests.resources.test_support.low.helpers import resource


class BaseTelescopeControl(object):
    """Base Telescope control class.
    Use this class to write method to check status of devices
    """

    def is_in_valid_state(self, device_state_info, state_str, wait_time=10):
        """Validate device state is in desired state as per device state info
        Args:
            device_state_info (dict): device name and it's expected state info
        """
        elapsed_time = 0
        start_time = time.time()
        while elapsed_time < wait_time:
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
            if all(state_result_list):
                return True
            elapsed_time = time.time() - start_time
            time.sleep(0.1)
        return False
