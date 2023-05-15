# import json
# import time

# import pytest
# from pytest_bdd import given, parsers, scenario, then, when
# from tango import DeviceProxy

# from tests.conftest import LOGGER
# from tests.resources.test_support.common_utils.common_helpers import resource
# from tests.resources.test_support.common_utils.result_code import ResultCode
# from tests.resources.test_support.common_utils.tmc_helpers import (
#     TmcHelper,
#     tear_down,
# )
# from tests.resources.test_support.constant import (
#     DEVICE_OBS_STATE_EMPTY_INFO,
#     DEVICE_OBS_STATE_IDLE_INFO,
#     DEVICE_OBS_STATE_READY_INFO,
#     DEVICE_OBS_STATE_SCANNING_INFO,
#     DEVICE_STATE_ON_INFO,
#     DEVICE_STATE_STANDBY_INFO,
#     ON_OFF_DEVICE_COMMAND_DICT,
#     centralnode,
#     tmc_subarraynode1,
# )
# from tests.resources.test_support.telescope_controls import (
#     BaseTelescopeControl,
# )

# # noqa: E501
# tmc_helper = TmcHelper(centralnode, tmc_subarraynode1)
# telescope_control = BaseTelescopeControl()


# @pytest.mark.kk
# @pytest.mark.SKA_mid
# @scenario(
#     "../features/successful_scan_after_failed_assigned.feature",
#     "Successfully execute a scan after a failed attempt to assign resources",
# )
# def test_assign_resource_with_invalid_json():
#     """
#     Test AssignResource command with input as invalid json.

#     """
