import functools
from resources.test_support.helpers import waiter, watch, resource
from contextlib import contextmanager
import signal
import logging
from contextlib import contextmanager


# def check_coming_out_of_standby():
#     ##Can  only start up a disabled telescope
#     resource("ska_mid/tm_subarray_node/1").assert_attribute("State").equals("OFF")

# def check_going_into_standby():
#     print("In check_going_into_standby")
#     resource("ska_mid/tm_subarray_node/1").assert_attribute("State").equals("ON")


def sync_telescope_on(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # check_coming_out_of_standby()
        the_waiter = waiter()
        the_waiter.set_wait_for_telescope_on()
        result = func(*args, **kwargs)
        the_waiter.wait(50)
        return result

    return wrapper


# defined as a context manager
@contextmanager
def sync_telescope_on(timeout=50):
    # check_coming_out_of_standby()
    the_waiter = waiter()
    the_waiter.set_wait_for_telescope_on()
    yield
    the_waiter.wait(timeout)


def sync_set_to_off(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # check_going_into_standby()
        the_waiter = waiter()
        the_waiter.set_wait_for_going_to_off()
        result = func(*args, **kwargs)
        the_waiter.wait(100)
        return result

    return wrapper


# defined as a context manager
@contextmanager
def sync_going_to_off(timeout=50):
    # check_going_into_standby()
    the_waiter = waiter()
    the_waiter.set_wait_for_going_to_off()
    yield
    the_waiter.wait(timeout)
