import functools
from tests.resources.test_support.common_utils.common_helpers import Waiter
from contextlib import contextmanager
from tests.conftest import TIMEOUT


def sync_telescope_on(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        the_waiter = Waiter(**kwargs)
        the_waiter.set_wait_for_telescope_on()
        result = func(*args, **kwargs)
        the_waiter.wait(TIMEOUT)
        return result

    return wrapper

def sync_set_to_off(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        the_waiter = Waiter(**kwargs)
        the_waiter.set_wait_for_going_to_off()
        result = func(*args, **kwargs)
        the_waiter.wait(TIMEOUT)
        return result

    return wrapper

# defined as a context manager
@contextmanager
def sync_going_to_off(timeout=50, **kwargs):
    the_waiter = Waiter(**kwargs)
    the_waiter.set_wait_for_going_to_off()
    yield
    the_waiter.wait(timeout)


def sync_set_to_standby(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        the_waiter = Waiter(**kwargs)
        the_waiter.set_wait_for_going_to_standby()
        result = func(*args, **kwargs)
        the_waiter.wait(TIMEOUT)
        return result

    return wrapper

def sync_release_resources(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        the_waiter = Waiter(**kwargs)
        the_waiter.set_wait_for_going_to_empty()
        result = func(*args, **kwargs)
        the_waiter.wait(TIMEOUT)
        return result

    return wrapper

