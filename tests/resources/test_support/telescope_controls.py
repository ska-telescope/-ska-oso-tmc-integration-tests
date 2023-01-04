from tests.resources.test_support.low.helpers import (
    resource
)
from tests.conftest import LOGGER

class BaseTelescopeControl(object):
    """

    Args:
        object (_type_): _description_
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
            LOGGER.info(f'resource({device}).get("{state_str}") ' + device_state)
            state_result_list.append(resource(device).get(state_str) in state_list)
        
        return all(state_result_list)
    
    # def telescope_is_in_standby_state(self, device_state_info=None):
    #     return self.is_in_valid_state(device_state_info, "State")

    # def telescope_is_in_on_state(self, device_state_info):
    #     return self.is_in_valid_state(device_state_info, "State")
    
    # def telescope_is_in_off_state(self, device_state_info):
    #     return self.is_in_valid_state(device_state_info, "State")
    #     # LOGGER.info(
    #     #     'resource(sdp_master).get("State")'
    #     #     + str(resource(sdp_master).get("State"))
    #     # )
    #     # LOGGER.info(
    #     #     'resource(sdp_subarray1).get("State")'
    #     #     + str(resource(sdp_subarray1).get("State"))
    #     # )
    #     # LOGGER.info(
    #     #     'resource(csp_master).get("State")'
    #     #     + str(resource(csp_master).get("State"))
    #     # )
    #     # LOGGER.info(
    #     #     'resource(csp_subarray1).get("State")'
    #     #     + str(resource(csp_subarray1).get("State"))
    #     # )
    #     # LOGGER.info(
    #     #     'resource(dish_master1).get("State")'
    #     #     + str(resource(dish_master1).get("State"))
    #     # )

        # return [
        #     resource(sdp_subarray1).get("State"),
        #     resource(sdp_master).get("State"),
        #     resource(csp_master).get("State"),
        #     resource(csp_subarray1).get("State"),
        #     resource(dish_master1).get("State"),
        # ] == ["OFF", "OFF", "OFF", "OFF", "STANDBY"]
