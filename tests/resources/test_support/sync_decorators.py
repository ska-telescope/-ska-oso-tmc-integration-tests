import functools
from tests.resources.test_support.helpers import waiter, resource
from contextlib import contextmanager


# pre checks
def check_going_out_of_empty():
    # verify once for obstate = EMPTY
    resource("mid-csp/subarray/01").assert_attribute("obsState").equals("EMPTY")
    resource("mid_sdp/elt/subarray_1").assert_attribute("obsState").equals("EMPTY")
    resource("ska_mid/tm_subarray_node/1").assert_attribute("obsState").equals("EMPTY")

def sync_telescope_on(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        the_waiter = waiter()
        the_waiter.set_wait_for_telescope_on()
        result = func(*args, **kwargs)
        the_waiter.wait(500)
        return result

    return wrapper

def sync_set_to_off(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        the_waiter = waiter()
        the_waiter.set_wait_for_going_to_off()
        result = func(*args, **kwargs)
        the_waiter.wait(500)
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
        the_waiter.wait(500)
        return result

    return wrapper

def sync_release_resources(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        the_waiter = waiter()
        the_waiter.set_wait_for_going_to_empty()
        result = func(*args, **kwargs)
        the_waiter.wait(500)
        return result

    return wrapper
  
def sync_assign_resources():
    # defined as a decorator
    def decorator_sync_assign_resources(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            check_going_out_of_empty()
            the_waiter = waiter()
            the_waiter.set_wait_for_assign_resources()
            result = func(*args, **kwargs)
            the_waiter.wait(500)
            return result

        return wrapper

    return decorator_sync_assign_resources