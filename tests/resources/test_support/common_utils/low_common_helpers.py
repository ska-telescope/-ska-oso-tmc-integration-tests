from tests.resources.test_support.common_utils.common_helpers import watch, resource, Waiter
from tests.resources.test_support.constant_low import sdp_subarray1, csp_subarray1, tmc_subarraynode1, csp_master, sdp_master

# this is a composite type of waiting based on a set of predefined pre conditions expected to be true
class LowWaiter(Waiter):
    """Waiter class for low which override necessary methods for low
    """

    def set_wait_for_going_to_off(self):
        self.waits.append(
            watch(resource(sdp_subarray1)).to_become(
                "State", changed_to="OFF"
            )
        )
        self.waits.append(
            watch(resource(sdp_master)).to_become(
                "State", changed_to="OFF"
            )
        )
        self.waits.append(
            watch(resource(csp_subarray1)).to_become(
                "State", changed_to="OFF"
            )
        )
        self.waits.append(
            watch(resource(csp_master)).to_become(
                "State", changed_to="OFF"
            )
        )
    def set_wait_for_going_to_standby(self):
        self.waits.append(
            watch(resource(sdp_subarray1)).to_become(
                "State", changed_to="OFF"
            )
        )
        self.waits.append(
            watch(resource(sdp_master)).to_become(
                "State", changed_to="STANDBY"
            )
        )
        self.waits.append(
            watch(resource(csp_subarray1)).to_become(
                "State", changed_to="OFF"
            )
        )
        self.waits.append(
            watch(resource(csp_master)).to_become(
                "State", changed_to="STANDBY"
            )
        )

    def set_wait_for_telescope_on(self):
        self.waits.append(
            watch(resource(sdp_master)).to_become("State", changed_to="ON")
        )
        self.waits.append(
            watch(resource(sdp_subarray1)).to_become(
                "State", changed_to="ON"
            )
        )
        self.waits.append(
            watch(resource(csp_master)).to_become("State", changed_to="ON")
        )
        self.waits.append(
            watch(resource(csp_subarray1)).to_become(
                "State", changed_to="ON"
            )
        )