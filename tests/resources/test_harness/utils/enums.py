"""Enum to used in tests
"""
from enum import IntEnum, unique


@unique
class DishMode(IntEnum):
    # ska-mid-dish-manager is having dependency conflicts with ska-tmc-common
    # So redefined DishMode enum, which reflects the ska-mid-dish-manager
    # DishMode enum.
    # We will work out on this separately once dish manager is sorted.
    STARTUP = 0
    SHUTDOWN = 1
    STANDBY_LP = 2
    STANDBY_FP = 3
    MAINTENANCE = 4
    STOW = 5
    CONFIG = 6
    OPERATE = 7
    UNKNOWN = 8


@unique
class SubarrayState(IntEnum):
    ON = 0
    OFF = 1
    FAULT = 8
    INIT = 9
    UNKNOWN = 13


@unique
class SubarrayObsState(IntEnum):
    EMPTY = 0
    RESOURCING = 1
    IDLE = 2
    CONFIGURING = 3
    READY = 4
    SCANNING = 5


@unique
class MockDeviceType(IntEnum):
    CSP_DEVICE = 0
    SDP_DEVICE = 1
