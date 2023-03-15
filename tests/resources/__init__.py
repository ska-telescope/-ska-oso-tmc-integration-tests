import os
from tests.resources.test_support.base_utils import BaseTestUtils

ENV = os.getenv("TELESCOPE")

if ENV == "SKA-mid":
    from tests.resources.test_support.constant import csp_subarray1, sdp_subarray1, tmc_subarraynode1
    test_utils = BaseTestUtils(obs_state_device_names = [
        csp_subarray1, sdp_subarray1, tmc_subarraynode1
    ])

elif ENV == "SKA-low":
    from tests.resources.test_support.constant_low import csp_subarray1, sdp_subarray1, tmc_subarraynode1
    test_utils = BaseTestUtils(obs_state_device_names = [
        csp_subarray1, sdp_subarray1, tmc_subarraynode1
    ])