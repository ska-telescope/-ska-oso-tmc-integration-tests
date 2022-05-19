from os.path import dirname, join
from tests.resources.test_support.sync_decorators import (
    sync_telescope_on,
    sync_set_to_off,
    sync_set_to_standby,
    sync_release_resources,
)
from tango import DeviceProxy
from tests.resources.test_support.controls import centralnode

import logging

LOGGER = logging.getLogger(__name__)


def get_input_str(input_file):
    path = join(dirname(__file__), "..", "..", "data", input_file)
    with open(path, "r") as f:
        return f.read()


@sync_telescope_on
def set_to_on():
    CentralNode = DeviceProxy(centralnode)
    LOGGER.info(
        "Before Sending TelescopeOn command on CentralNode state :"
        + str(CentralNode.State())
    )
    CentralNode.TelescopeOn()


@sync_set_to_off
def set_to_off():
    CentralNode = DeviceProxy(centralnode)
    CentralNode.TelescopeOff()
    LOGGER.info(
            f"After invoking TelescopeOff command {centralnode} State is: {CentralNode.State()}"
    )

@sync_set_to_standby
def set_to_standby():
    CentralNode = DeviceProxy(centralnode)
    CentralNode.TelescopeStandBy()
    LOGGER.info(
            f"After invoking TelescopeStandBy command {centralnode} State is: {CentralNode.State()}"
    )


@sync_release_resources
def invoke_releaseResources(release_input_str):
    CentralNode = DeviceProxy(centralnode)
    CentralNode.ReleaseResources(release_input_str)
    LOGGER.info("ReleaseResources is invoked on Central Node")
