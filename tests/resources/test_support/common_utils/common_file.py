# from tango import DeviceProxy

# import tests.resources.test_support.tmc_helpers as tmc
# from tests.conftest import LOGGER

# from tests.resources.test_support.controls import (
#     subarray_obs_state_is_empty,
#     subarray_obs_state_is_idle,
#     subarray_obs_state_is_ready,
#     telescope_is_in_off_state,
#     telescope_is_in_on_state,
#     telescope_is_in_standby_state,
# )
# from tests.resources.test_support.helpers import resource
# from tests.resources.test_support.sync_decorators import (
#     sync_assign_resources,
#     sync_configure,
#     sync_end,
# )

# configure_resources_file = "command_Configure.json"


# def send_commands():
#     """Invoke Configure() Command on TMC"""
#     try:
#         LOGGER.info("Invoking Configure command on TMC CentralNode")
#         configure_input = tmc.get_input_str(configure_resources_file)
#         subarray_node = DeviceProxy("ska_mid/tm_subarray_node/1")
#         subarray_node.Configure(configure_input)
#         LOGGER.info("Invoked Configure on SubarrayNode")
#     except:
#         LOGGER.info("CONFIGURE COMMAND NOT VALID IN EMPTY ObsState ")
#     # finally:
#     #     LOGGER.info('Checking if telescope is ON and in EMPTY obsState')
#     #     assert telescope_is_in_on_state()
#     #     assert subarray_obs_state_is_empty()
