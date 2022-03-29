# pylint: disable=unused-argument
import pytest
import tango
from tango.test_context import MultiDeviceTestContext
from tango.test_utils import DeviceTestContext



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


@pytest.fixture
def sdp_master_device():
    return "mid_sdp/elt/master"


@pytest.fixture
def csp_master_device():
    return "mid_csp/elt/master"


@pytest.fixture(scope="session")
def sdp_subarray_device():
    return "mid_sdp/elt/subarray_1"
