"""
This module has custom exception for repository ska_tmc_subarraynode
"""


class InvalidObsStateError(ValueError):
    """Raised when subarray is not in required obsState."""


class CommandNotAllowed(Exception):
    """Raised when a command is not allowed."""