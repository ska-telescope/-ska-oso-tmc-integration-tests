import json
from os.path import dirname, join
from tests.resources.test_support.sync_decorators import (
    sync_set_to_assign_resources,
    sync_telescope_on,
    sync_set_to_off,
    sync_set_to_standby,
    sync_release_resources,
)
from tango import DeviceProxy
from tests.resources.test_support.helpers import waiter, watch, resource

import logging

LOGGER = logging.getLogger(__name__)


def get_input_str(input_file):
    path = join(dirname(__file__), "..", "..", "data", input_file)
    with open(path, "r") as f:
        input_str = f.read()
    return json.dumps(input_str)


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
def set_to_assign_resources(assign_input_str):
    CentralNode = DeviceProxy("ska_mid/tm_central/central_node")
    CentralNode.AssignResources(assign_input_str)
    LOGGER.info("AssignResources is invoked")

@sync_release_resources
def invoke_releaseResources(release_input_str):
    CentralNode = DeviceProxy("ska_mid/tm_central/central_node")
    CentralNode.ReleaseResources(release_input_str)
    LOGGER.info("ReleaseResources is invoked")
