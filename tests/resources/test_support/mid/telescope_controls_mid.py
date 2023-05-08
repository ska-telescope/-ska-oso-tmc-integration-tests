"""_summary_
"""
from tests.resources.test_support.telescope_controls import (
    BaseTelescopeControl,
)


class TelescopeControlMid(BaseTelescopeControl):
    """
    Now all method related to telescope control are common for both low and mid
    but created placeholder class for low so in case method required for low
    can be written here or overridden
    """
