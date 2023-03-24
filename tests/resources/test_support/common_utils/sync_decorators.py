import functools
from tests.resources.test_support.helpers import resource, WaitForScan
from tests.resources.test_support.common_utils.low_common_helpers import LowWaiter
from tests.resources.test_support.common_utils.common_helpers import Waiter
from contextlib import contextmanager
import tests.resources.test_support.tmc_helpers as tmc
from tests.settings import test_utils, ENV

def get_waiter_object():
    if ENV == "SKA-low":
        return LowWaiter()
    else:
        return Waiter()

def sync_telescope_on(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        the_waiter = get_waiter_object()
        the_waiter.set_wait_for_telescope_on()
        result = func(*args, **kwargs)
        the_waiter.wait(200)
        return result

    return wrapper

def sync_set_to_off(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        the_waiter = get_waiter_object()
        the_waiter.set_wait_for_going_to_off()
        result = func(*args, **kwargs)
        the_waiter.wait(200)
        return result

    return wrapper

# defined as a context manager
@contextmanager
def sync_going_to_off(timeout=50):
    the_waiter = get_waiter_object()
    the_waiter.set_wait_for_going_to_off()
    yield
    the_waiter.wait(timeout)


def sync_set_to_standby(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        the_waiter = get_waiter_object()
        the_waiter.set_wait_for_going_to_standby()
        result = func(*args, **kwargs)
        the_waiter.wait(200)
        return result

    return wrapper

def sync_release_resources(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        the_waiter = get_waiter_object()
        the_waiter.set_wait_for_going_to_empty()
        result = func(*args, **kwargs)
        the_waiter.wait(200)
        return result

    return wrapper

def sync_assign_resources():
    # defined as a decorator
    def decorator_sync_assign_resources(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # check_going_out_of_empty()
            test_utils.check_going_out_of_obsState("EMPTY")
            the_waiter = get_waiter_object()
            # Added this check to ensure that devices are running to avoid random test failures.
            tmc.check_devices()
            the_waiter.set_wait_for_assign_resources()
            result = func(*args, **kwargs)
            the_waiter.wait(200)
            return result

        return wrapper

    return decorator_sync_assign_resources

def sync_configure():
    # defined as a decorator
    def decorator_sync_configure(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # check_resources_assign()
            test_utils.check_going_out_of_obsState("IDLE")
            the_waiter = get_waiter_object()
            # Added this check to ensure that devices are running to avoid random test failures.
            tmc.check_devices()
            the_waiter.set_wait_for_configure()
            result = func(*args, **kwargs)
            the_waiter.wait(500)
            return result

        return wrapper

    return decorator_sync_configure

def sync_configure_abort():
    # defined as a decorator
    def decorator_sync_configure_abort(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # check_resources_assign()
            test_utils.check_going_out_of_obsState("IDLE")
            # Added this check to ensure that devices are running to avoid random test failures.
            tmc.check_devices()
            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator_sync_configure_abort

def sync_scan(timeout = 300):
    # define as a decorator
    def decorator_sync_scan(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # check_going_out_of_configure()
            test_utils.check_going_out_of_obsState("READY")
            scan_wait = WaitForScan()
            result = func(*args, **kwargs)
            scan_wait.wait(timeout)
            return result

        return wrapper

    return decorator_sync_scan

def sync_end():
    # defined as a decorator
    def decorator_sync_end(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # check_going_out_of_configure()
            test_utils.check_going_out_of_obsState("READY")
            the_waiter = get_waiter_object()
            the_waiter.set_wait_for_idle()
            result = func(*args, **kwargs)
            the_waiter.wait(500)
            return result

        return wrapper

    return decorator_sync_end


def sync_abort(timeout = 300):
    # define as a decorator
    def decorator_sync_abort(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            the_waiter = get_waiter_object()
            the_waiter.set_wait_for_aborted()
            result = func(*args, **kwargs)
            the_waiter.wait(timeout)
            return result

        return wrapper

    return decorator_sync_abort


def sync_restart(timeout = 300):
    # define as a decorator
    def decorator_sync_restart(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # check_going_out_of_abort()
            test_utils.check_going_out_of_obsState("ABORTED")
            the_waiter = get_waiter_object()
            the_waiter.set_wait_for_going_to_empty()
            result = func(*args, **kwargs)
            the_waiter.wait(timeout)
            return result

        return wrapper

    return decorator_sync_restart
