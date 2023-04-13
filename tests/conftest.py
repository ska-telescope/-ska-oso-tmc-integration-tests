from typing import Optional
import pytest
import logging
from os.path import dirname, join
import tango
import os
import tests.resources.test_support.tmc_helpers as tmc
from tests.resources.test_support.helpers import resource
from tests.resources.test_support.constant import (
    tmc_subarraynode1,
    centralnode
)
from tests.resources.test_support.controls import (
    subarray_obs_state_is_aborted,
    subarray_obs_state_is_empty,
    subarray_obs_state_is_idle,
    telescope_is_in_standby_state,
)

LOGGER = logging.getLogger(__name__)


def pytest_sessionstart(session):
    """
    Pytest hook; prints info about tango version.
    :param session: a pytest Session object
    :type session: :py:class:`pytest.Session`
    """
    print(tango.utils.info())


def pytest_addoption(parser):
    """
    Pytest hook; implemented to add the `--true-context` option, used to
    indicate that a true Tango subsystem is available, so there is no
    need for a :py:class:`tango.test_context.MultiDeviceTestContext`.
    :param parser: the command line options parser
    :type parser: :py:class:`argparse.ArgumentParser`
    """
    parser.addoption(
        "--true-context",
        action="store_true",
        default=False,
        help=(
            "Tell pytest that you have a true Tango context and don't "
            "need to spin up a Tango test context"
        ),
    )


def get_input_str(path):
    """
    Returns input json string
    :rtype: String
    """
    with open(path, "r") as f:
        input_arg = f.read()
    return input_arg


@pytest.fixture()
def json_factory():
    """
    Json factory for getting json files
    """

    def _get_json(slug):
        return get_input_str(join(dirname(__file__), "data", f"{slug}.json"))

    return _get_json

TELESCOPE_ENV = os.getenv("TELESCOPE")

TIMEOUT = 200


def tear_down(input_json: Optional[str] = None):
    """Tears down the system after test run to get telescope back in standby state."""
    subarray_node_obsstate = resource(tmc_subarraynode1).get("obsState")

    if subarray_node_obsstate in ["RESOURCING", "CONFIGURING", "SCANNING"]:
        LOGGER.info("Invoking Abort on TMC")
        tmc.invoke_abort()

        assert subarray_obs_state_is_aborted()

        LOGGER.info("Invoking Restart on TMC")
        tmc.invoke_restart()

        assert subarray_obs_state_is_empty()

        LOGGER.info("Invoking Telescope Standby on TMC")
        tmc.set_to_standby()

        assert telescope_is_in_standby_state()
        LOGGER.info("Tear Down complete. Telescope is in Standby State")

    elif subarray_node_obsstate == "EMPTY":
        LOGGER.info("Invoking Telescope Standby on TMC")
        tmc.set_to_standby()

        assert telescope_is_in_standby_state()
        LOGGER.info("Tear Down complete. Telescope is in Standby State")

    elif subarray_node_obsstate == "IDLE":
        LOGGER.info("Invoking ReleaseResources on TMC")
        tmc.invoke_releaseResources(input_json)

        LOGGER.info("Invoking Telescope Standby on TMC")
        tmc.set_to_standby()

        assert telescope_is_in_standby_state()
        LOGGER.info("Tear Down complete. Telescope is in Standby State")

    elif subarray_node_obsstate == "READY":
        LOGGER.info("Invoking END on TMC")
        tmc.end()

        assert subarray_obs_state_is_idle()

        LOGGER.info("Invoking ReleaseResources on TMC")
        tmc.invoke_releaseResources(input_json)

        LOGGER.info("Invoking Telescope Standby on TMC")
        tmc.set_to_standby()

        assert telescope_is_in_standby_state()
        LOGGER.info("Tear Down complete. Telescope is in Standby State")

    elif subarray_node_obsstate == "EMPTY":
        LOGGER.info("Invoking Telescope Standby on TMC")
        tmc.set_to_standby()

        assert telescope_is_in_standby_state()
        LOGGER.info("Tear Down complete. Telescope is in Standby State")
