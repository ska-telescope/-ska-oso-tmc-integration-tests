from tests.resources.test_support.sync_decorators import (
    sync_set_to_assign_resources,
    sync_telescope_on,
    sync_set_to_off,
    sync_set_to_standby,
    sync_set_to_assign_resources,
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
    LOGGER.info("Off the Telescope")

@sync_set_to_standby
def set_to_standby():
    CentralNode = DeviceProxy("ska_mid/tm_central/central_node")
    CentralNode.TelescopeStandBy()
    LOGGER.info("After TelescopeStandBy CentralNode State:" + str(CentralNode.State()))
    LOGGER.info("Off the Telescope")

@sync_set_to_assign_resources
def set_to_assign_resources():
    CentralNode = DeviceProxy("ska_mid/tm_central/central_node")
    CentralNode.AssignResources()
    LOGGER.info("After AssignResources CentralNode ObState:" + str(CentralNode.State()))
    LOGGER.info("Assign Resources")