import functools
from contextlib import contextmanager

from tests.conftest import TIMEOUT
from tests.resources.test_support.common_utils.base_utils import DeviceUtils
from tests.resources.test_support.common_utils.common_helpers import Waiter


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


def sync_assign_resources():
    # defined as a decoratorW
    def decorator_sync_assign_resources(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
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


def sync_abort(timeout=300):
    # define as a decorator
    def decorator_sync_abort(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            the_waiter = Waiter(**kwargs)
            the_waiter.set_wait_for_aborted()
            result = func(*args, **kwargs)
            the_waiter.wait(timeout)
            return result

        return wrapper

    return decorator_sync_abort


def sync_restart(timeout=300):
    # define as a decorator
    def decorator_sync_restart(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
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
    # defined as a decorator
    def decorator_sync_configure(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            device = DeviceUtils(
                obs_state_device_names=[
                    kwargs.get("csp_subarray"),
                    kwargs.get("sdp_subarray"),
                    kwargs.get("tmc_subarraynode"),
                ]
            )
            device.check_devices_obsState("IDLE")
            the_waiter = Waiter(**kwargs)
            the_waiter.set_wait_for_configure()
            result = func(*args, **kwargs)
            the_waiter.wait(500)
            return result

        return wrapper

    return decorator_sync_configure


def sync_end():
    # defined as a decorator
    def decorator_sync_end(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
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

    return decorator_sync_end

def sync_reconfigure(timeout=500):
    # defined as a decorator
    def decorator_sync_reconfigure(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            device = DeviceUtils(
                obs_state_device_names=[
                    kwargs.get("csp_subarray"),
                    kwargs.get("sdp_subarray"),
                    kwargs.get("tmc_subarraynode"),
                ]
            )
            device.check_devices_obsState("READY")
            print("sync reconfigure, Ready check success")
            the_waiter = Waiter(**kwargs)
            # the_waiter.set_wait_for_configuring()
            the_waiter.set_wait_for_configure()
            result = func(*args, **kwargs)
            the_waiter.wait(timeout)
            print("sync reconfigure, Ready check success")
            return result
        return wrapper
    return decorator_sync_reconfigure