"""State Resetter class
"""
from tests.resources.test_harness.utils.common_utils import JsonFactory


class StateResetter(object):
    """ """

    def __init__(self, name, device):
        self.name = name
        self.device = device

        self.json_factory = JsonFactory()
        self.assign_input = self.json_factory.create_assign_resource(
            "assign_resources_mid"
        )
        self.configure_input = self.json_factory.create_subarray_configuration(
            "configure_mid"
        )
        self.scan_input = self.json_factory.create_subarray_configuration(
            "scan_mid"
        )


class ReadyStateResetter(StateResetter):
    """
    Put self.device into the "READY" state
    and reset the relevant values (resources and configurations)
    """

    state_name = "READY"

    def reset(self):
        self.device.clear_all_data()
        self.device.store_resources(self.assign_input)
        self.device.store_configuration_data(self.configure_input)


class IdleStateResetter(StateResetter):
    """
    Put self.device into the "IDLE" state
    and reset the relevant values (resources)
    """

    state_name = "IDLE"

    def reset(self):
        self.device.clear_all_data()
        self.device.store_resources(self.assign_input)


class EmptyStateResetter(StateResetter):
    """
    Put self.device into the "EMPTY" state
    """

    state_name = "EMPTY"

    def reset(self):
        self.device.clear_all_data()


class ResourcingStateResetter(StateResetter):
    """
    Put self.device into the "RESOURCING" state
    """

    state_name = "RESOURCING"

    def reset(self):
        self.device.clear_all_data()
        self.device.execute_transition(
            command_name="AssignResources", argin=self.assign_input
        )


class ConfiguringStateResetter(StateResetter):
    """
    Put self.device into the "CONFIGURING" state
    """

    state_name = "CONFIGURING"

    def reset(self):
        self.device.clear_all_data()
        self.device.store_resources(self.assign_input)
        self.device.execute_transition(
            command_name="Configure", argin=self.configure_input
        )


class AbortingStateResetter(StateResetter):
    """
    Put self.device into the "ABORTING" state
    """

    state_name = "ABORTING"

    def reset(self):
        self.device.clear_all_data()
        self.device.store_resources(self.assign_input)
        self.device.execute_transition(command_name="Abort", argin=None)


class AbortedStateResetter(StateResetter):
    """
    Put self.device into the "ABORTED" state
    """

    state_name = "ABORTED"

    def reset(self):
        self.device.clear_all_data()
        self.device.store_resources(self.assign_input)
        self.device.abort_subarray()


class ScanningStateResetter(StateResetter):
    """
    Put self.device into the "ABORTED" state
    """

    state_name = "SCANNING"

    def reset(self):
        self.device.clear_all_data()
        self.device.store_resources(self.assign_input)
        self.device.store_configuration_data(self.configure_input)
        self.device.store_scan_data(self.scan_input)


class StateResetterFactory:
    table = {
        "EMPTY": EmptyStateResetter,
        "RESOURCING": ResourcingStateResetter,
        "IDLE": IdleStateResetter,
        "CONFIGURING": ConfiguringStateResetter,
        "READY": ReadyStateResetter,
        "ABORTING": AbortingStateResetter,
        "ABORTED": AbortedStateResetter,
        "SCANNING": ScanningStateResetter,
    }

    def create_state_resetter(self, state_name, device):
        state_resetter = self.table[state_name](state_name, device)
        return state_resetter
