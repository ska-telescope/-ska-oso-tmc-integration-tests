import pytest

# from pytest_bdd import given, parsers, scenario, then, when
from tango import DeviceProxy

from tests.conftest import LOGGER
from tests.resources.test_support.constant import tmc_subarraynode1


@pytest.mark.unavail
@pytest.mark.SKA_mid
# @scenario(
#     "../features/test_device_unavailability.feature",
#     "Check availibility of CSPleafnode",
# )
def test_check_device_unavailability():
    """
    Test TMC subsystems availability.

    """
    # creating subarray device proxy
    subarray_node = DeviceProxy(tmc_subarraynode1)

    # Reading isSubarrayAvailable attribute value
    value = subarray_node.read_attribute("isSubarrayAvailable").value
    LOGGER.info(f"Subarray value:::{value}")

    assert value


# @pytest.mark.unavail1
# @pytest.mark.SKA_mid
# def test_CSPleafnode_unavailability():
#     """
#     Test TMC subsystems availability.

#     """
#     # creating subarray device proxy
#     subarray_node = DeviceProxy(tmc_subarraynode1)
#     csp_subarray = DeviceProxy(tmc_csp_subarray_leaf_node)
#     sdp_subarray = DeviceProxy(tmc_sdp_subarray_leaf_node)

#     # Reading isSubarrayAvailable attribute value
#     value = subarray_node.read_attribute("isSubarrayAvailable").value
#     csp_value = csp_subarray.read_attribute("isSubsystemAvailable").value
#     sdp_value = sdp_subarray.read_attribute("isSubsystemAvailable").value

#     LOGGER.info(f"Subarray value:::{value}")
#     LOGGER.info(f"CSP value:::{csp_value}")
#     LOGGER.info(f"SDP value:::{sdp_value}")
#     assert value


# @pytest.mark.unavail
# @pytest.mark.SKA_mid

# def test_check_device_unavailability():
#     """
#     Test TMC subsystems availability.

#     """
#     # creating subarray device proxy
#     central_node = DeviceProxy(centralnode)

#     # Reading isSubarrayAvailable attribute value
#     value = central_node.read_attribute("telescopeAvailability").value
#     assert value
