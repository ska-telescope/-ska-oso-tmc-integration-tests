"""TMC Class which contain method specific to TMC
"""
from tango import DeviceProxy

from tests.resources.test_harness.constant import (
    tmc_csp_master_leaf_node,
    tmc_dish_leaf_node1,
    tmc_dish_leaf_node2,
    tmc_dish_leaf_node3,
    tmc_dish_leaf_node4,
)

from .central_node_mid import CentralNodeWrapperMid


class TMCMid:
    def __init__(self):
        """Set all devices proxy required for TMC"""
        self.central_node = CentralNodeWrapperMid()
        self.csp_master_leaf_node = DeviceProxy(tmc_csp_master_leaf_node)
        self.csp_master_ln_server = DeviceProxy(
            f"dserver/{self.csp_master_leaf_node.info().server_id}"
        )
        self.central_node_server = DeviceProxy(
            f"dserver/{self.central_node.central_node.info().server_id}"
        )
        self.dish_leaf_node_list = [
            DeviceProxy(tmc_dish_leaf_node1),
            DeviceProxy(tmc_dish_leaf_node2),
            DeviceProxy(tmc_dish_leaf_node3),
            DeviceProxy(tmc_dish_leaf_node4),
        ]

    @property
    def IsDishVccConfigSet(self):
        """ """
        return self.central_node.IsDishVccConfigSet

    @property
    def DishVccValidationStatus(self):
        """Current dish vcc validation status of central node"""
        return self.central_node.DishVccValidationStatus

    def RestartServer(self, server_type: str):
        """Restart server based on provided server type"""
        if server_type == "CSP_MLN":
            self.csp_master_ln_server.RestartServer()
        elif server_type == "CENTRAL_NODE":
            self.central_node_server.RestartServer()
        elif server_type.startswith("DISH_"):
            dish_id = int(server_type.split("_")[-1]) - 1
            dish_proxy = self.dish_leaf_node_list[int(dish_id)]
            dish_server = DeviceProxy(f"dserver/{dish_proxy.info().server_id}")
            dish_server.RestartServer()

    def load_dish_vcc_configuration(self, dish_vcc_config):
        """Load Dish Vcc config on TMC"""
        return self.central_node.load_dish_vcc_configuration(dish_vcc_config)

    def tear_down(self):
        """tear down"""
        self.central_node.tear_down()
