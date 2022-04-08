from tests.resources.test_support.sync_decorators import (
    sync_telescope_on,
    sync_set_to_off,
)
from tango import DeviceProxy
from tests.resources.test_support.helpers import waiter, watch, resource

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
    # LOGGER.info("After TelescopeOff CentralNode telescopeState:" + str(CentralNode.telescopeState()))
    LOGGER.info("Off the Telescope")
