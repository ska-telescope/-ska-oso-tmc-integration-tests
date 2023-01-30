import functools
from tests.resources.test_support.low.helpers import waiter, resource, WaitForScan
from contextlib import contextmanager
from tests.resources.test_support.constant_low import csp_subarray1, sdp_subarray1, tmc_subarraynode1

# pre checks
def check_going_out_of_empty():
    # verify once for obstate = EMPTY
    resource(csp_subarray1).assert_attribute("obsState").equals("EMPTY")
    resource(sdp_subarray1).assert_attribute("obsState").equals("EMPTY")
    resource(tmc_subarraynode1).assert_attribute("obsState").equals("EMPTY")


def check_resources_assign():
    # verify once for obstate = IDLE
    resource(csp_subarray1).assert_attribute("obsState").equals("IDLE")
    resource(sdp_subarray1).assert_attribute("obsState").equals("IDLE")
    resource(tmc_subarraynode1).assert_attribute("obsState").equals("IDLE")


def check_going_out_of_configure():
    # verify once for obstate = READY
    resource(csp_subarray1).assert_attribute("obsState").equals("READY")
    resource(sdp_subarray1).assert_attribute("obsState").equals("READY")
    resource(tmc_subarraynode1).assert_attribute("obsState").equals("READY")


def sync_telescope_on(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        the_waiter = waiter()
        the_waiter.set_wait_for_telescope_on()
        result = func(*args, **kwargs)
        the_waiter.wait(200)
        return result

    return wrapper

def sync_set_to_off(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        the_waiter = waiter()
        the_waiter.set_wait_for_going_to_off()
        result = func(*args, **kwargs)
        the_waiter.wait(200)
        return result

    return wrapper

# defined as a context manager
@contextmanager
def sync_going_to_off(timeout=50):
    the_waiter = waiter()
    the_waiter.set_wait_for_going_to_off()
    yield
    the_waiter.wait(timeout)


def sync_set_to_standby(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        the_waiter = waiter()
        the_waiter.set_wait_for_going_to_standby()
        result = func(*args, **kwargs)
        the_waiter.wait(200)
        return result

    return wrapper

def sync_release_resources():
    def decorator_sync_assign_resources(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            the_waiter = waiter()
            the_waiter.set_wait_for_going_to_empty()
            result = func(*args, **kwargs)
            the_waiter.wait(200)
            return result

        return wrapper

    return decorator_sync_assign_resources

def sync_assign_resources():
    # defined as a decorator
    def decorator_sync_assign_resources(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            check_going_out_of_empty()
            the_waiter = waiter()
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
            check_resources_assign()
            the_waiter = waiter()
            the_waiter.set_wait_for_configure()
            result = func(*args, **kwargs)
            the_waiter.wait(500)
            return result

        return wrapper

    return decorator_sync_configure

def sync_scan(timeout = 300):
    # define as a decorator
    def decorator_sync_scan(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            check_going_out_of_configure()
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
            check_going_out_of_configure()
            the_waiter = waiter()
            the_waiter.set_wait_for_idle()
            result = func(*args, **kwargs)
            the_waiter.wait(500)
            return result

        return wrapper

    return decorator_sync_end
