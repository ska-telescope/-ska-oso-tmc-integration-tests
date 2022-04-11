import functools
from tests.resources.test_support.helpers import waiter
from contextlib import contextmanager


def sync_telescope_on(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        the_waiter = waiter()
        the_waiter.set_wait_for_telescope_on()
        result = func(*args, **kwargs)
        the_waiter.wait(100)
        return result

    return wrapper


def sync_set_to_off(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        the_waiter = waiter()
        the_waiter.set_wait_for_going_to_off()
        result = func(*args, **kwargs)
        the_waiter.wait(100)
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
        the_waiter.wait(100)
        return result

    return wrapper