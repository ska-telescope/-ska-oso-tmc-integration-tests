"""Test module for TMC-DISH testing"""

import logging
import os
import time

import pytest
from pytest_bdd import given, scenario, then, when
from tango import DeviceProxy, DevState
from tango.db import Database, DbDevInfo

from tests.resources.test_support.enum import DishMode

LOGGER = logging.getLogger(__name__)


class TestCentralNodeRobustness(object):
    def __init__(self):
        self.dish1_dev_name = os.getenv("DISH_NAME_1")
        self.dish36_dev_name = os.getenv("DISH_NAME_36")
        self.dish63_dev_name = os.getenv("DISH_NAME_63")
        self.dish100_dev_name = os.getenv("DISH_NAME_100")

        # Create database object for TMC TANGO DB
        self.db = Database()

        # Create database object for Dish1 TANGO DB
        self.dish1_tango_host = self.dish1_dev_name.split("/")[2]
        self.dish1_host = self.dish1_tango_host.split(":")[0]
        self.dish1_port = self.dish1_tango_host.split(":")[1]
        self.dish1_db = Database(self.dish1_host, self.dish1_port)

        # Fetch information of the TMC devices from the TANGO db
        sdp_master_dev_info = self.db.get_device_info("mid-sdp/control/0")
        csp_master_dev_info = self.db.get_device_info("mid-csp/control/0")
        central_node_info = self.db.get_device_info(
            "ska_mid/tm_central/central_node"
        )
        dish_leaf_node1_info = self.db.get_device_info(
            "ska_mid/tm_leaf_node/d0001"
        )
        dish_leaf_node36_info = self.db.get_device_info(
            "ska_mid/tm_leaf_node/d0036"
        )
        dish_leaf_node63_info = self.db.get_device_info(
            "ska_mid/tm_leaf_node/d0063"
        )
        dish_leaf_node100_info = self.db.get_device_info(
            "ska_mid/tm_leaf_node/d0100"
        )

        # Create proxies of the TMC devices
        self.csp_master_proxy = DeviceProxy(csp_master_dev_info.name)
        self.dp_master_proxy = DeviceProxy(sdp_master_dev_info.name)
        self.centralnode_proxy = DeviceProxy(central_node_info.name)
        self.dish_leaf_node1_proxy = DeviceProxy(dish_leaf_node1_info.name)
        self.dish_leaf_node36_proxy = DeviceProxy(dish_leaf_node36_info.name)
        self.dish_leaf_node63_proxy = DeviceProxy(dish_leaf_node63_info.name)
        self.dish_leaf_node100_proxy = DeviceProxy(dish_leaf_node100_info.name)

        # Create proxies of the Dish devices
        self.dish1_proxy = DeviceProxy(self.dish1_dev_name)
        self.dish36_proxy = DeviceProxy(self.dish36_dev_name)
        self.dish63_proxy = DeviceProxy(self.dish63_dev_name)
        self.dish100_proxy = DeviceProxy(self.dish100_dev_name)

        # Create Dish1 admin device proxy
        self.dish1_admin_dev_name = self.dish1_proxy.adm_name()
        self.dish1_admin_dev_proxy = DeviceProxy(self.dish1_admin_dev_name)

        # Get the Dish1 device class and server
        self.dish1_info = self.dish1_db.get_device_info("ska001/elt/master")
        self.dish1_dev_class = self.dish1_info.class_name
        self.dish1_dev_server = self.dish1_info.ds_full_name

        # Create Dish1 admin device proxy
        self.dish1_leaf_admin_dev_name = self.dish_leaf_node1_proxy.adm_name()
        self.dish1_leaf_admin_dev_proxy = DeviceProxy(
            self.dish1_leaf_admin_dev_name
        )

    @pytest.mark.tmc_dish
    @scenario(
        "../features/tmc_dish/xtp-29077.feature",
        "Mid TMC Central Node robustness test with disappearing DishLMC",
    )
    def test_tmc_central_node_robustness(self):
        """
        Test case to verify TMC CentralNode Robustness
        """

    @given("a Telescope consisting of TMC, DISH, CSP and SDP")
    def given_telescope(self):
        """
        Given a Telescope with TMC, Dish, CSP and SDP systems

        Args:
            - "event_recorder": fixture for EventRecorder class
        """
        assert self.centralnode_proxy.ping() > 0
        assert self.csp_master_proxy.ping() > 0
        assert self.sdp_master_proxy.ping() > 0
        assert self.dish1_proxy.ping() > 0
        assert self.dish36_proxy.ping() > 0
        assert self.dish63_proxy.ping() > 0
        assert self.dish100_proxy.ping() > 0

    @given(
        "dishes with Dish IDs 001, 036, 063, 100 are registered on the TangoDB"
    )
    def given_the_dishes_registered_in_tango_db(self):
        """
        Given the dishes are registered in the TANGO Database
        """
        assert self.dish1_proxy.dev_name() == "ska001/elt/master"
        assert self.dish36_proxy.dev_name() == "ska036/elt/master"
        assert self.dish63_proxy.dev_name() == "ska063/elt/master"
        assert self.dish100_proxy.dev_name() == "ska100/elt/master"

    @given(
        "dishleafnodes for dishes with IDs 001, 036, 063, 100 are available"
    )
    def check_if_dish_leaf_nodes_alive(self):
        """A method to check if the dish leaf nodes are alive"""

        assert self.dish_leaf_node1_proxy.ping() > 0
        assert self.dish_leaf_node36_proxy.ping() > 0
        assert self.dish_leaf_node63_proxy.ping() > 0
        assert self.dish_leaf_node100_proxy.ping() > 0

    @given("command TelescopeOn was sent and received by the dishes")
    def move_telescope_to_on_state(self):
        """A method to put Telescope to ON state"""

        self.verify_the_dishes_are_in_standbylp_state()

        LOGGER.info("Invoke TelescopeOn() on all sub-systems")
        self.centralnode_proxy.TelescopeOn()
        assert self.wait_and_validate_device_attribute_value(
            self.dish1_proxy, "dishMode", DishMode.STANDBY_FP
        )
        assert self.wait_and_validate_device_attribute_value(
            self.dish36_proxy, "dishMode", DishMode.STANDBY_FP
        )
        assert self.wait_and_validate_device_attribute_value(
            self.dish63_proxy, "dishMode", DishMode.STANDBY_FP
        )
        assert self.wait_and_validate_device_attribute_value(
            self.dish100_proxy, "dishMode", DishMode.STANDBY_FP
        )
        assert self.wait_and_validate_device_attribute_value(
            self.centralnode_proxy, "telescopeState", DevState.ON
        )

    @when("communication with Dish ID 001 is lost")
    def fail_to_connect_dish(self):
        """A method to create the dish connection failure"""
        LOGGER.info(
            "dish1 admin device name is: %s", self.dish1_admin_dev_name
        )
        LOGGER.info("dish1 device name is: %s", self.dish1_dev_name)

        check_dish1_info = self.dish1_db.get_device_info("ska001/elt/master")
        LOGGER.info("check_dish1_info is: %s", check_dish1_info)

        self.dish1_db.delete_device(self.dish1_dev_name)
        self.dish1_admin_dev_proxy.RestartServer()
        # Added a wait for the completion of dish device deletion from TANGO
        # database and the dish device restart
        time.sleep(2)

    @when("command TelescopeOff is sent")
    def invoke_telescope_off_command(self):
        """A method to put Telescope to OFF state"""
        LOGGER.info("Invoke TelescopeOff command")
        self.centralnode_proxy.TelescopeOff()

        assert self.wait_and_validate_device_attribute_value(
            self.dish36_proxy, "dishMode", DishMode.STANDBY_LP
        )
        assert self.wait_and_validate_device_attribute_value(
            self.dish63_proxy, "dishMode", DishMode.STANDBY_LP
        )
        assert self.wait_and_validate_device_attribute_value(
            self.dish100_proxy, "dishMode", DishMode.STANDBY_LP
        )
        assert self.wait_and_validate_device_attribute_value(
            self.centralnode_proxy, "telescopeState", DevState.OFF
        )
        LOGGER.info("The telescopeState is OFF")

    @then("the Central Node is still running")
    def check_if_central_node_running(self):
        """Method to check if central node is still running"""
        assert self.centralnode_proxy.ping() > 0
        LOGGER.info("CentralNode is running")

    @then("Dish with ID 001 comes back")
    def connect_to_dish(self):
        """Method to restablish the connection with the lost dish"""
        # Add Dish device back to DB
        dev_info = DbDevInfo()
        dev_info.name = self.dish1_dev_name
        dev_info._class = self.dish1_dev_class
        dev_info.server = self.dish1_dev_server
        self.dish1_db.add_device(dev_info)

        self.dish1_admin_dev_proxy.RestartServer()
        self.dish1_leaf_admin_dev_proxy.RestartServer()

        # When device restart it will at least take 10 sec to up again
        # so added 10 sec sleep.
        time.sleep(10)

        # Check if the dish 1 is initialised
        assert self.wait_and_validate_device_attribute_value(
            self.dish1_proxy, "dishMode", DishMode.STANDBY_FP
        )
        check_dish1_info = self.dish1_db.get_device_info("ska001/elt/master")
        LOGGER.info("dish1 device info is: %s", check_dish1_info)
        check_dish1_leaf_info = self.db.get_device_info(
            "ska_mid/tm_leaf_node/d0001"
        )
        LOGGER.info(
            "dish1 leaf node device info is: %s", check_dish1_leaf_info
        )

    @then("command TelescopeOff can be sent and received by the dish")
    def move_telescope_to_off_state(self):
        """A method to put Telescope to OFF state"""
        LOGGER.info("Invoke TelescopeOff() with all real sub-systems")
        self.centralnode_proxy.TelescopeOff()

    @then("the Central Node is still running")
    def recheck_if_central_node_running(self):
        assert self.centralnode_proxy.ping() > 0

    @then("the telescope is in OFF state")
    def check_if_telescope_is_in_off_state(self):
        assert self.wait_and_validate_device_attribute_value(
            self.dish36_proxy, "dishMode", DishMode.STANDBY_LP
        )
        assert self.wait_and_validate_device_attribute_value(
            self.dish63_proxy, "dishMode", DishMode.STANDBY_LP
        )
        assert self.wait_and_validate_device_attribute_value(
            self.dish100_proxy, "dishMode", DishMode.STANDBY_LP
        )
        assert self.wait_and_validate_device_attribute_value(
            self.dish1_proxy, "dishMode", DishMode.STANDBY_LP
        )
        LOGGER.info(
            "Dish %s dishMode is: %s",
            self.dish1_dev_name,
            self.dish1_proxy.dishMode,
        )
        assert self.wait_and_validate_device_attribute_value(
            self.centralnode_proxy, "telescopeState", DevState.OFF
        )

    def verify_the_dishes_are_in_standbylp_state(self):
        assert self.wait_and_validate_device_attribute_value(
            self.dish1_proxy, "dishMode", DishMode.STANDBY_LP
        )
        assert self.wait_and_validate_device_attribute_value(
            self.dish36_proxy, "dishMode", DishMode.STANDBY_LP
        )
        assert self.wait_and_validate_device_attribute_value(
            self.dish63_proxy, "dishMode", DishMode.STANDBY_LP
        )
        assert self.wait_and_validate_device_attribute_value(
            self.dish100_proxy, "dishMode", DishMode.STANDBY_LP
        )

    def wait_and_validate_device_attribute_value(
        self,
        device: DeviceProxy,
        attribute_name: str,
        expected_value: str,
        timeout: int = 70,
    ):
        """This method wait and validate if attribute value is equal to
        provided expected value
        """
        count = 0
        error = ""
        while count <= timeout:
            try:
                attribute_value = device.read_attribute(attribute_name).value
                if attribute_value:
                    logging.info(
                        "%s current %s value: %s",
                        device.name(),
                        attribute_name,
                        attribute_value,
                    )
                if attribute_value == expected_value:
                    return True
            except Exception as e:
                # In case the device gets unavailable due to restart. Then the
                # above command tries to access the attribute resulting into
                # exception. It keeps it printing till the attribute is
                # accessible.The exception log is suppressed by storing into
                # variable. the error is printed later into the log in case
                # of failure
                error = e
            count += 1
            time.sleep(1)

        logging.exception(
            "Exception occurred while reading attribute %s and cnt is %s",
            error,
            count,
        )
        return False
