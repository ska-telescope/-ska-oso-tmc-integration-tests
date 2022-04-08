from resources.test_support.sync_decorators import (
    sync_telescope_on,
    sync_set_to_off,
    sync_configure,
    sync_end_sb,
    sync_release_resources,
    sync_set_to_standby,
    time_it,
    sync_abort,
    sync_restart,
    sync_obsreset,
)
from resources.test_support.logging_decorators import log_it
from tango import DeviceProxy
from resources.test_support.helpers import waiter, watch, resource
from resources.test_support.controls import telescope_is_in_standby
from resources.test_support.persistance_helping import (
    load_config_from_file,
    update_scan_config_file,
    update_resource_config_file,
)

import logging

LOGGER = logging.getLogger(__name__)


@sync_telescope_on
def set_to_on():
    CentralNode = DeviceProxy("ska_mid/tm_central/central_node")
    LOGGER.info(
        "Before Sending TelescopeOn command on CentralNode state :"
        + str(CentralNode.State())
    )
    CentralNode.TelescopeOn()


@sync_set_to_off
def set_to_off():
    CentralNode = DeviceProxy("ska_mid/tm_central/central_node")
    CentralNode.TelescopeOff()
    LOGGER.info("After TelescopeOff CentralNode State:" + str(CentralNode.State()))
    LOGGER.info("After TelescopeOff CentralNode telescopeState:" + str(CentralNode.telescopeState()))
    LOGGER.info("Off the Telescope")
