"""Test module for TMC-DISH """

import logging
import os
import time

import pytest
from pytest_bdd import given, parsers, scenario, then, when
from tango import DeviceProxy, DevState
from tango.db import Database, DbDevInfo

from tests.resources.test_support.enum import DishMode

LOGGER = logging.getLogger(__name__)

dish1_dev_name = os.getenv("DISH_NAME_1")
dish36_dev_name = os.getenv("DISH_NAME_36")
dish63_dev_name = os.getenv("DISH_NAME_63")
dish100_dev_name = os.getenv("DISH_NAME_100")

# Create database object for TMC TANGO DB
db = Database()

# Create database object for Dish1 TANGO DB
dish1_tango_host = dish1_dev_name.split("/")[2]
dish1_host = dish1_tango_host.split(":")[0]
dish1_port = dish1_tango_host.split(":")[1]
dish1_db = Database(dish1_host, dish1_port)

# Fetch information of the TMC devices from the TANGO db
sdp_master_dev_info = db.get_device_info("mid-sdp/control/0")
csp_master_dev_info = db.get_device_info("mid-csp/control/0")
central_node_info = db.get_device_info("ska_mid/tm_central/central_node")
dish_leaf_node1_info = db.get_device_info("ska_mid/tm_leaf_node/d0001")
dish_leaf_node36_info = db.get_device_info("ska_mid/tm_leaf_node/d0036")
dish_leaf_node63_info = db.get_device_info("ska_mid/tm_leaf_node/d0063")
dish_leaf_node100_info = db.get_device_info("ska_mid/tm_leaf_node/d0100")

# Get the full names of the  TMC devices from device info received from
# TANGO db
sdp_master_dev_name = sdp_master_dev_info.name
csp_master_dev_name = csp_master_dev_info.name
central_node_dev_name = central_node_info.name
dish_leaf_node1_dev_name = dish_leaf_node1_info.name
dish_leaf_node36_dev_name = dish_leaf_node36_info.name
dish_leaf_node63_dev_name = dish_leaf_node63_info.name
dish_leaf_node100_dev_name = dish_leaf_node100_info.name

# Create proxies of the TMC devices
csp_master_proxy = DeviceProxy(csp_master_dev_name)
sdp_master_proxy = DeviceProxy(sdp_master_dev_name)
centralnode_proxy = DeviceProxy(central_node_dev_name)
dish_leaf_node1_proxy = DeviceProxy(dish_leaf_node1_dev_name)
dish_leaf_node36_proxy = DeviceProxy(dish_leaf_node36_dev_name)
dish_leaf_node63_proxy = DeviceProxy(dish_leaf_node63_dev_name)
dish_leaf_node100_proxy = DeviceProxy(dish_leaf_node100_dev_name)

# Create proxies of the Dish devices
dish1_proxy = DeviceProxy(dish1_dev_name)
dish36_proxy = DeviceProxy(dish36_dev_name)
dish63_proxy = DeviceProxy(dish63_dev_name)
dish100_proxy = DeviceProxy(dish100_dev_name)

# Create Dish1 admin device proxy
dish1_admin_dev_name = dish1_proxy.adm_name()
dish1_admin_dev_proxy = DeviceProxy(dish1_admin_dev_name)

# Get the Dish1 device class and server
dish1_info = dish1_db.get_device_info("ska001/elt/master")
dish1_dev_class = dish1_info.class_name
dish1_dev_server = dish1_info.ds_full_name

# Create Dish1 admin device proxy
dish1_leaf_admin_dev_name = dish_leaf_node1_proxy.adm_name()
dish1_leaf_admin_dev_proxy = DeviceProxy(dish1_leaf_admin_dev_name)


def verify_the_telescope_is_in_off_state(event_recorder):
    event_recorder.subscribe_event(dish1_proxy, "dishMode")
    event_recorder.subscribe_event(dish36_proxy, "dishMode")
    event_recorder.subscribe_event(dish63_proxy, "dishMode")
    event_recorder.subscribe_event(dish100_proxy, "dishMode")
    event_recorder.subscribe_event(centralnode_proxy, "telescopeState")

    assert event_recorder.has_change_event_occurred(
        dish1_proxy,
        "dishMode",
        DishMode.STANDBY_LP,
    )
    assert event_recorder.has_change_event_occurred(
        dish36_proxy,
        "dishMode",
        DishMode.STANDBY_LP,
    )
    assert event_recorder.has_change_event_occurred(
        dish63_proxy,
        "dishMode",
        DishMode.STANDBY_LP,
    )
    assert event_recorder.has_change_event_occurred(
        dish100_proxy,
        "dishMode",
        DishMode.STANDBY_LP,
    )

    # Wait for the DishLeafNode to get StandbyLP event form DishMaster before
    # invoking TelescopeOn command
    # time.sleep(1)
    # assert event_recorder.has_change_event_occurred(
    #     centralnode_proxy,
    #     "telescopeState",
    #     DevState.OFF,
    # )


def wait_and_validate_device_attribute_value(
    device: DeviceProxy,
    attribute_name: str,
    expected_value: str,
    timeout: int = 70,
):
    """This method wait and validate if attribute value is equal to provided
    expected value
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
            # Device gets unavailable due to restart and the above command
            # tries to access the attribute resulting into exception
            # It keeps it printing till the attribute is accessible
            # the exception log is suppressed by storing into variable
            # the error is printed later into the log in case of failure
            error = e
        count += 10
        # When device restart it will at least take 10 sec to up again
        # so added 10 sec sleep and to avoid frequent attribute read.
        time.sleep(10)

    logging.exception(
        "Exception occurred while reading attribute %s and cnt is %s",
        error,
        count,
    )
    return False


@pytest.mark.tmc_dish
@scenario(
    "../features/tmc_dish/xtp-29077.feature",
    "Mid TMC Central Node robustness test with disappearing DishLMC",
)
def test_tmc_central_node_robustness():
    """
    Test case to verify TMC CentralNode Robustness
    """


@given("a Telescope consisting of TMC, DISH, CSP and SDP")
def given_telescope():
    """
    Given a Telescope with TMC, Dish, CSP and SDP systems

    Args:
        - "event_recorder": fixture for EventRecorder class
    """
    assert centralnode_proxy.ping() > 0
    assert csp_master_proxy.ping() > 0
    assert sdp_master_proxy.ping() > 0
    assert dish1_proxy.ping() > 0
    assert dish36_proxy.ping() > 0
    assert dish63_proxy.ping() > 0
    assert dish100_proxy.ping() > 0


@given(
    parsers.parse(
        "dishes with Dish IDs {dish_ids} are registered on the TangoDB"
    )
)
def given_the_dishes_registered_in_tango_db(dish_ids):
    """
    Given the dishes are registered in the TANGO Database
    """
    dishes = dish_ids.split(",")
    LOGGER.info("dishes: %s", dishes)
    assert dish1_proxy.dev_name() == "ska001/elt/master"
    assert dish36_proxy.dev_name() == "ska036/elt/master"
    assert dish63_proxy.dev_name() == "ska063/elt/master"
    assert dish100_proxy.dev_name() == "ska100/elt/master"


@given(
    parsers.parse("dishleafnodes for dishes with IDs {dish_ids} are available")
)
def check_if_dish_leaf_nodes_alive(dish_ids):
    """A method to put Telescope to ON state"""
    dishes = dish_ids.split(",")
    LOGGER.info("dishes: %s", dishes)

    assert dish_leaf_node1_proxy.ping() > 0
    assert dish_leaf_node36_proxy.ping() > 0
    assert dish_leaf_node63_proxy.ping() > 0
    assert dish_leaf_node100_proxy.ping() > 0


@given("command TelescopeOn was sent and received by the dishes")
def move_telescope_to_on_state(event_recorder):
    """A method to put Telescope to ON state"""

    verify_the_telescope_is_in_off_state(event_recorder)

    LOGGER.info("Invoke TelescopeOn() on all sub-systems")
    centralnode_proxy.TelescopeOn()

    assert event_recorder.has_change_event_occurred(
        dish1_proxy,
        "dishMode",
        DishMode.STANDBY_FP,
    )
    assert event_recorder.has_change_event_occurred(
        dish36_proxy,
        "dishMode",
        DishMode.STANDBY_FP,
    )
    assert event_recorder.has_change_event_occurred(
        dish63_proxy,
        "dishMode",
        DishMode.STANDBY_FP,
    )
    assert event_recorder.has_change_event_occurred(
        dish100_proxy,
        "dishMode",
        DishMode.STANDBY_FP,
    )

    # # Wait for the DishLeafNode to get StandbyFP events
    # time.sleep(1)
    assert event_recorder.has_change_event_occurred(
        centralnode_proxy,
        "telescopeState",
        DevState.ON,
    )


@when(parsers.parse("communication with Dish ID {test_dish_id} is lost"))
def fail_to_connect_dish(test_dish_id):
    """A method to create dish connection failure"""

    LOGGER.info("test_dish_id: %s", test_dish_id)
    LOGGER.info("dish1_admin_dev_name is: %s", dish1_admin_dev_name)
    LOGGER.info("dish1_dev_name: %s", dish1_dev_name)

    check_dish1_info = dish1_db.get_device_info("ska001/elt/master")
    LOGGER.info("check_dish1_info is: %s", check_dish1_info)
    dish1_db.delete_device(dish1_dev_name)
    dish1_admin_dev_proxy.RestartServer()
    # Added a wait for the completion of dish device name deletion from
    # database and the dish device restart
    time.sleep(2)


@when("command TelescopeOff is sent")
def invoke_telescope_off_command(event_recorder):
    LOGGER.info("Invoke TelescopeOff command")
    centralnode_proxy.TelescopeOff()
    assert event_recorder.has_change_event_occurred(
        dish36_proxy,
        "dishMode",
        DishMode.STANDBY_LP,
    )
    assert event_recorder.has_change_event_occurred(
        dish63_proxy,
        "dishMode",
        DishMode.STANDBY_LP,
    )
    assert event_recorder.has_change_event_occurred(
        dish100_proxy,
        "dishMode",
        DishMode.STANDBY_LP,
    )
    assert event_recorder.has_change_event_occurred(
        centralnode_proxy,
        "telescopeState",
        DevState.OFF,
    )
    LOGGER.info("telescopeState is OFF")


@then("the Central Node is still running")
def check_if_central_node_running():
    """Method to check if central node is still running"""
    assert centralnode_proxy.ping() > 0
    LOGGER.info("CentralNode is running")


@then(parsers.parse("Dish with ID {test_dish_id} comes back"))
def connect_to_dish(test_dish_id):
    """Method to restablish the connection with the lost dish"""
    LOGGER.info("test_dish_id: %s", test_dish_id)

    # Add Dish device back to DB
    dev_info = DbDevInfo()
    dev_info.name = dish1_dev_name
    dev_info._class = dish1_dev_class
    dev_info.server = dish1_dev_server
    dish1_db.add_device(dev_info)

    dish1_admin_dev_proxy.RestartServer()
    dish1_leaf_admin_dev_proxy.RestartServer()
    check_dish1_info = dish1_db.get_device_info("ska001/elt/master")
    LOGGER.info("check_dish1_info is: %s", check_dish1_info)
    check_dish1_leaf_info = db.get_device_info("ska_mid/tm_leaf_node/d0001")
    LOGGER.info("check_dish1_leaf_info is: %s", check_dish1_leaf_info)
    # Wait for the dish addition in the TANGO database and device restart
    assert wait_and_validate_device_attribute_value(
        dish1_proxy, "dishMode", DishMode.STANDBY_FP
    )

    # time.sleep(20)

    check_dish1_info = dish1_db.get_device_info("ska001/elt/master")
    LOGGER.info("check_dish1_info is: %s", check_dish1_info)
    check_dish1_leaf_info = db.get_device_info("ska_mid/tm_leaf_node/d0001")
    LOGGER.info("check_dish1_leaf_info is: %s", check_dish1_leaf_info)


@then("command TelescopeOff can be sent and received by the dish")
def move_telescope_to_off_state():
    LOGGER.info("Invoke TelescopeOff() with all real sub-systems")
    centralnode_proxy.TelescopeOff()


@then("the Central Node is still running")
def recheck_if_central_node_running(event_recorder):
    assert centralnode_proxy.ping() > 0


@then("the telescope is in OFF state")
def check_if_telescope_is_in_off_state(event_recorder):
    assert event_recorder.has_change_event_occurred(
        dish36_proxy,
        "dishMode",
        DishMode.STANDBY_LP,
    )
    assert event_recorder.has_change_event_occurred(
        dish63_proxy,
        "dishMode",
        DishMode.STANDBY_LP,
    )
    assert event_recorder.has_change_event_occurred(
        dish100_proxy,
        "dishMode",
        DishMode.STANDBY_LP,
    )

    # Wait for the DishLeafNode to get StandbyLP event form DishMaster
    # time.sleep(1)
    assert event_recorder.has_change_event_occurred(
        centralnode_proxy,
        "telescopeState",
        DevState.OFF,
    )
    # dish1_proxy = DeviceProxy(dish1_dev_name)
    LOGGER.info(
        "Dish %s dishMode is: %s", dish1_dev_name, dish1_proxy.dishMode
    )
    event_recorder.subscribe_event(dish1_proxy, "dishMode")
    assert event_recorder.has_change_event_occurred(
        dish1_proxy,
        "dishMode",
        DishMode.STANDBY_LP,
    )
