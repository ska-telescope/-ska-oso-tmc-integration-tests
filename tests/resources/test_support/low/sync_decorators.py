"""this modules contains decorators for sync methods """
import functools
from contextlib import contextmanager

from tests.resources.test_support.constant_low import (
    csp_subarray1,
    sdp_subarray1,
    tmc_subarraynode1,
)
from tests.resources.test_support.low.helpers import (
    WaitForScan,
    resource,
    waiter,
)


# pre checks
def check_going_out_of_empty():
    """verify once for obstate = EMPTY"""
    resource(csp_subarray1).assert_attribute("obsState").equals("EMPTY")
    resource(sdp_subarray1).assert_attribute("obsState").equals("EMPTY")
    resource(tmc_subarraynode1).assert_attribute("obsState").equals("EMPTY")


def check_resources_assign():
    """verify once for obstate = IDLE"""
    resource(csp_subarray1).assert_attribute("obsState").equals("IDLE")
    resource(sdp_subarray1).assert_attribute("obsState").equals("IDLE")
    resource(tmc_subarraynode1).assert_attribute("obsState").equals("IDLE")


def check_going_out_of_configure():
    """verify once for obstate = READY"""
    resource(csp_subarray1).assert_attribute("obsState").equals("READY")
    resource(sdp_subarray1).assert_attribute("obsState").equals("READY")
    resource(tmc_subarraynode1).assert_attribute("obsState").equals("READY")


def sync_telescope_on(func):
    """sync method for telescope on"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """wrapper method"""
        the_waiter = waiter()
        the_waiter.set_wait_for_telescope_on()
        result = func(*args, **kwargs)
        the_waiter.wait(200)
        return result

    return wrapper


def sync_set_to_off(func):
    """sync method for telescope off"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """wrapper method"""
        the_waiter = waiter()
        the_waiter.set_wait_for_going_to_off()
        result = func(*args, **kwargs)
        the_waiter.wait(200)
        return result

    return wrapper


# defined as a context manager
@contextmanager
def sync_going_to_off(timeout=50):
    """context manager method for syncing telescope to off"""
    the_waiter = waiter()
    the_waiter.set_wait_for_going_to_off()
    yield
    the_waiter.wait(timeout)


def sync_set_to_standby(func):
    """context manager method for syncing telescope to standby"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """wrapper for sync telescope to standby"""
        the_waiter = waiter()
        the_waiter.set_wait_for_going_to_standby()
        result = func(*args, **kwargs)
        the_waiter.wait(200)
        return result

    return wrapper


def sync_release_resources(func):
    """wrapper for syncing method to release resources"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """wrapper method"""
        the_waiter = waiter()
        the_waiter.set_wait_for_going_to_empty()
        result = func(*args, **kwargs)
        the_waiter.wait(200)
        return result

    return wrapper


def sync_assign_resources():
    """method for syncing assign resources
    defined as a decorator"""

    def decorator_sync_assign_resources(func):
        """decorator method"""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """wrapper method"""
            check_going_out_of_empty()
            the_waiter = waiter()
            the_waiter.set_wait_for_assign_resources()
            result = func(*args, **kwargs)
            the_waiter.wait(200)
            return result

        return wrapper

    return decorator_sync_assign_resources


def sync_configure():
    """method for syncing configure command
    defined as a decorator"""

    def decorator_sync_configure(func):
        """decorator method"""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """wrapper method"""
            check_resources_assign()
            the_waiter = waiter()
            the_waiter.set_wait_for_configure()
            result = func(*args, **kwargs)
            the_waiter.wait(500)
            return result

        return wrapper

    return decorator_sync_configure


def sync_scan(timeout: int = 300):
    """method for syncing scan command
    defined as a decorator"""

    def decorator_sync_scan(func):
        """decorator method"""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """wrapper method"""
            check_going_out_of_configure()
            scan_wait = WaitForScan()
            result = func(*args, **kwargs)
            scan_wait.wait(timeout)
            return result

        return wrapper

    return decorator_sync_scan


def sync_end():
    """method for syncing end command
    defined as a decorator"""

    def decorator_sync_end(func):
        """decorator method"""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """wrapper method"""
            check_going_out_of_configure()
            the_waiter = waiter()
            the_waiter.set_wait_for_idle()
            result = func(*args, **kwargs)
            the_waiter.wait(500)
            return result

        return wrapper

    return decorator_sync_end
