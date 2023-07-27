"""This modules contains decorators for sync methods """
import functools
import logging
from contextlib import contextmanager

from tests.conftest import TIMEOUT
from tests.resources.test_support.common_utils.base_utils import DeviceUtils
from tests.resources.test_support.common_utils.common_helpers import (
    Waiter,
    WaitForScan,
    resource,
)

LOGGER = logging.getLogger(__name__)


def sync_telescope_on(func):
    """sync method for telescope on"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """wrapper method"""
        the_waiter = Waiter(**kwargs)
        the_waiter.set_wait_for_telescope_on()
        result = func(*args, **kwargs)
        the_waiter.wait(TIMEOUT)
        return result

    return wrapper


def sync_set_to_off(func):
    """wrapper for telescope off"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """wrapper method"""
        the_waiter = Waiter(**kwargs)
        the_waiter.set_wait_for_going_to_off()
        result = func(*args, **kwargs)
        the_waiter.wait(TIMEOUT)
        return result

    return wrapper


# defined as a context manager
@contextmanager
def sync_going_to_off(timeout=50, **kwargs):
    """context manager method for syncing telescope to off"""
    the_waiter = Waiter(**kwargs)
    the_waiter.set_wait_for_going_to_off()
    yield
    the_waiter.wait(timeout)


def sync_set_to_standby(func):
    """wrapper for sync telescope to standby"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """wrapper method"""
        the_waiter = Waiter(**kwargs)
        the_waiter.set_wait_for_going_to_standby()
        result = func(*args, **kwargs)
        the_waiter.wait(TIMEOUT)
        return result

    return wrapper


def sync_release_resources():
    """wrapper for syncing method to release resources"""

    def decorator_sync_assign_resources(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """wrapper method"""
            result = func(*args, **kwargs)
            set_wait_for_obsstate = kwargs.get("set_wait_for_obsstate", True)
            if set_wait_for_obsstate:
                the_waiter = Waiter(**kwargs)
                the_waiter.set_wait_for_going_to_empty()
                the_waiter.wait(TIMEOUT)
            return result

        return wrapper

    return decorator_sync_assign_resources


def sync_assign_resources():
    """method for syncing assign resources
    defined as a decorator"""

    def decorator_sync_assign_resources(func):
        """decorator"""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """wrapper method"""
            set_wait_for_obsstate = kwargs.get("set_wait_for_obsstate", True)
            result = func(*args, **kwargs)
            if set_wait_for_obsstate:
                the_waiter = Waiter(**kwargs)
                the_waiter.set_wait_for_assign_resources()
                the_waiter.wait(200)
            return result

        return wrapper

    return decorator_sync_assign_resources


def sync_abort(timeout: int = 300):
    """sync method for abort command
    define as a decorator"""

    def decorator_sync_abort(func):
        """decorator method"""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """wrapper method"""
            the_waiter = Waiter(**kwargs)
            the_waiter.set_wait_for_aborted()
            result = func(*args, **kwargs)
            the_waiter.wait(timeout)
            return result

        return wrapper

    return decorator_sync_abort


def sync_restart(timeout: int = 300):
    """sync method for Restart Command
    define as a Decorator"""

    def decorator_sync_restart(func):
        """decorator"""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """wrapper method"""
            device = DeviceUtils(
                obs_state_device_names=[
                    kwargs.get("csp_subarray"),
                    kwargs.get("sdp_subarray"),
                    kwargs.get("tmc_subarraynode"),
                ]
            )
            device.check_devices_obsState("ABORTED")
            the_waiter = Waiter(**kwargs)
            the_waiter.set_wait_for_going_to_empty()
            result = func(*args, **kwargs)
            the_waiter.wait(timeout)
            return result

        return wrapper

    return decorator_sync_restart


def sync_configure():
    """sync method for configure command
    define as a decorator"""

    def decorator_sync_configure(func):
        """decorator"""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """wrapper method"""
            invoked_from_ready = False
            the_waiter = Waiter(**kwargs)
            if resource(kwargs.get("tmc_subarraynode")) == "READY":
                invoked_from_ready = True
            result = func(*args, **kwargs)
            set_wait_for_obsstate = kwargs.get("set_wait_for_obsstate", True)
            if set_wait_for_obsstate:
                if invoked_from_ready:
                    the_waiter.set_wait_for_configuring()
                    the_waiter.wait(500)
                the_waiter.set_wait_for_configure()
                the_waiter.wait(500)
            return result

        return wrapper

    return decorator_sync_configure


def sync_end():
    """sync method for end command
    define as a decorator"""

    def decorator_sync_end(func):
        """decorator method"""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """wrapper method"""
            device = DeviceUtils(
                obs_state_device_names=[
                    kwargs.get("csp_subarray"),
                    kwargs.get("sdp_subarray"),
                    kwargs.get("tmc_subarraynode"),
                ]
            )
            device.check_devices_obsState("READY")
            the_waiter = Waiter(**kwargs)
            the_waiter.set_wait_for_idle()
            result = func(*args, **kwargs)
            the_waiter.wait(200)
            return result

        return wrapper

    return decorator_sync_end


def wait_assign():
    """wait for assign resource command to complete"""

    def decorator_sync_assign(func):
        """decorator method"""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """wrapper method"""
            the_waiter = Waiter(**kwargs)
            the_waiter.set_wait_for_idle()
            result = func(*args, **kwargs)
            the_waiter.wait(200)
            return result

        return wrapper

    return decorator_sync_assign


def sync_assigning():
    """sync method for assign resource"""

    def decorator_sync_assign_resources(func):
        """decorator method"""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """wrapper method"""
            device = DeviceUtils(
                obs_state_device_names=[
                    kwargs.get("csp_subarray"),
                    kwargs.get("sdp_subarray"),
                    kwargs.get("tmc_subarraynode"),
                ]
            )
            device.check_devices_obsState("EMPTY")
            the_waiter = Waiter(**kwargs)
            the_waiter.set_wait_for_assign_resources()
            result = func(*args, **kwargs)
            the_waiter.wait(200)
            return result

        return wrapper

    return decorator_sync_assign_resources


def sync_configure_sub():
    """sync method for configure command"""

    def decorator_sync_configure(func):
        """decorator method"""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """wrapper method"""
            flag = False
            the_waiter = Waiter(**kwargs)
            if resource(kwargs.get("tmc_subarraynode")) == "READY":
                flag = True
            result = func(*args, **kwargs)
            if flag:
                the_waiter.set_wait_for_configuring()
                the_waiter.wait(500)
            the_waiter.set_wait_for_configure()
            the_waiter.wait(500)
            return result

        return wrapper

    return decorator_sync_configure


def sync_scan(timeout=500):
    """sync method for scan command"""

    def decorator_sync_scan(func):
        """decorator method"""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """wrapper method"""
            set_wait_for_obsstate = kwargs.get("set_wait_for_obsstate", True)
            device = DeviceUtils(
                obs_state_device_names=[
                    kwargs.get("csp_subarray"),
                    kwargs.get("sdp_subarray"),
                    kwargs.get("tmc_subarraynode"),
                ]
            )

            if set_wait_for_obsstate:
                device.check_devices_obsState("READY")
                scan_wait = WaitForScan(**kwargs)
                result = func(*args, **kwargs)
                scan_wait.wait(timeout)
            else:
                the_waiter = Waiter(**kwargs)
                result = func(*args, **kwargs)
                the_waiter.set_wait_for_scanning()
                the_waiter.wait(200)
            return result

        return wrapper

    return decorator_sync_scan


def sync_endscan():
    """sync method for endscan command"""

    def decorator_sync_end_scan(func):
        """decorator"""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """wrapper"""
            the_waiter = Waiter(**kwargs)
            the_waiter.set_wait_for_ready()
            result = func(*args, **kwargs)
            the_waiter.wait(200)
            return result

        return wrapper

    return decorator_sync_end_scan


def sync_endscan_in_ready():
    """defined as a decorator when endscan is invoked as invalid command"""

    def decorator_sync_end_scan(func):
        """decorator method"""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """wrapper method"""
            device = DeviceUtils(
                obs_state_device_names=[
                    kwargs.get("csp_subarray"),
                    kwargs.get("sdp_subarray"),
                    kwargs.get("tmc_subarraynode"),
                ]
            )
            device.check_devices_obsState("READY")
            the_waiter = Waiter(**kwargs)
            the_waiter.set_wait_for_idle()
            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator_sync_end_scan
