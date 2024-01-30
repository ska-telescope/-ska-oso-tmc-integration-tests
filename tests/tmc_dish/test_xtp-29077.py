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

REAL_DISH1_FQDN = os.getenv("DISH_NAME_1")
REAL_DISH36_FQDN = os.getenv("DISH_NAME_36")
REAL_DISH63_FQDN = os.getenv("DISH_NAME_63")
REAL_DISH100_FQDN = os.getenv("DISH_NAME_100")

dish_tango_host = os.getenv("DISH_TANGO_HOST")
dish_namespace1 = os.getenv("DISH_NAMESPACE_1")
cluster_domain = os.getenv("CLUSTER_DOMAIN")

db = Database()

# Fetch information of the devices from the TANGO db
sdp_master_dev_info = db.get_device_info("mid-sdp/control/0")
LOGGER.info("sdp_master_dev_info is: %s", sdp_master_dev_info)
csp_master_dev_info = db.get_device_info("mid-csp/control/0")
# dish36_info = db.get_device_info(REAL_DISH36_FQDN)
# dish63_info = db.get_device_info(REAL_DISH63_FQDN)
# dish100_info = db.get_device_info(REAL_DISH100_FQDN)
central_node_info = db.get_device_info("ska_mid/tm_central/central_node")
dish_leaf_node1_info = db.get_device_info("ska_mid/tm_leaf_node/d0001")
dish_leaf_node36_info = db.get_device_info("ska_mid/tm_leaf_node/d0036")
dish_leaf_node63_info = db.get_device_info("ska_mid/tm_leaf_node/d0063")
dish_leaf_node100_info = db.get_device_info("ska_mid/tm_leaf_node/d0100")

# Get the full names of the devices from device info received from TANGO db
sdp_master_dev_name = sdp_master_dev_info.name
LOGGER.info("sdp_master_dev_name is: %s", sdp_master_dev_name)
csp_master_dev_name = csp_master_dev_info.name
dish1_dev_name = REAL_DISH1_FQDN
LOGGER.info("dish1_dev_name is: %s", dish1_dev_name)
dish36_dev_name = REAL_DISH36_FQDN
dish63_dev_name = REAL_DISH63_FQDN
dish100_dev_name = REAL_DISH100_FQDN
central_node_dev_name = central_node_info.name
dish_leaf_node1_dev_name = dish_leaf_node1_info.name
dish_leaf_node36_dev_name = dish_leaf_node36_info.name
dish_leaf_node63_dev_name = dish_leaf_node63_info.name
dish_leaf_node100_dev_name = dish_leaf_node100_info.name

# Create proxies of the devices
csp_master_proxy = DeviceProxy(csp_master_dev_name)
LOGGER.info("csp_master_proxy is: %s", csp_master_proxy)
sdp_master_proxy = DeviceProxy(sdp_master_dev_name)
dish1_proxy = DeviceProxy(dish1_dev_name)
LOGGER.info("dish1_proxy is: %s", dish1_proxy)
dish36_proxy = DeviceProxy(dish36_dev_name)
dish63_proxy = DeviceProxy(dish63_dev_name)
dish100_proxy = DeviceProxy(dish100_dev_name)
centralnode_proxy = DeviceProxy(central_node_dev_name)

# def create_device_proxy(device_info):
#     full_dev_name = device_info.ds_full_name
#     dev_proxy = DeviceProxy(full_dev_name)
#     return dev_proxy

# Create dish1 admin device proxy
dish1_admin_dev_name = dish1_proxy.adm_name()
LOGGER.info("dish1_admin_dev_name is: %s", dish1_admin_dev_name)
dish1_admin_dev_proxy = DeviceProxy(dish1_admin_dev_name)
LOGGER.info("dish1_admin_dev_proxy is: %s", dish1_admin_dev_proxy)

# Get the Dish device class and server
dish1_info = dish1_proxy.info()
LOGGER.info("dish1_info is: %s", dish1_info)
dish1_dev_class = dish1_info.dev_class
LOGGER.info("dish1_dev_class is: %s", dish1_dev_class)
dish1_dev_server = dish1_info.server_id
LOGGER.info("dish1_dev_server is: %s", dish1_dev_server)


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
    time.sleep(1)
    # assert event_recorder.has_change_event_occurred(
    #     centralnode_proxy,
    #     "telescopeState",
    #     DevState.OFF,
    # )


@pytest.mark.tmc_dish
@scenario(
    "../features/tmc_dish/xtp-29077.feature",
    "Mid TMC Central Node robustness test with disappearing DishLMC",
)
def test_tmc_central_node_robustness():
    """
    Test case to verify TMC CentralNode Robustness
    """


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

    # Wait for the DishLeafNode to get StandbyFP events
    time.sleep(1)
    assert event_recorder.has_change_event_occurred(
        centralnode_proxy,
        "telescopeState",
        DevState.ON,
    )


@given(
    parsers.parse("dishleafnodes for dishes with IDs {dish_ids} are available")
)
def check_if_dish_leaf_nodes_alive(dish_ids):
    """A method to put Telescope to ON state"""
    dishes = dish_ids.split(",")
    LOGGER.info("dishes: %s", dishes)

    dish_leaf_node1_proxy = DeviceProxy(dish_leaf_node1_dev_name)
    dish_leaf_node36_proxy = DeviceProxy(dish_leaf_node36_dev_name)
    dish_leaf_node63_proxy = DeviceProxy(dish_leaf_node63_dev_name)
    dish_leaf_node100_proxy = DeviceProxy(dish_leaf_node100_dev_name)
    assert dish_leaf_node1_proxy.ping() > 0
    assert dish_leaf_node36_proxy.ping() > 0
    assert dish_leaf_node63_proxy.ping() > 0
    assert dish_leaf_node100_proxy.ping() > 0


@when(parsers.parse("communication with Dish ID {test_dish_id} is lost"))
def fail_to_connect_dish(test_dish_id):
    """A method to create dish connection failure"""

    LOGGER.info("test_dish_id: %s", test_dish_id)
    LOGGER.info("dish1_admin_dev_name is: %s", dish1_admin_dev_name)
    LOGGER.info("dish1_dev_name: %s", dish1_dev_name)

    dish_host = dish_tango_host + "." + dish_namespace1 + "." + cluster_domain
    LOGGER.info("dish_host is: %s", dish_host)
    dish_db = Database(dish_host, "10000")
    dish1_db_info = dish_db.get_device_info("ska001/elt/master")
    LOGGER.info("dish1_db_info is: %s", dish1_db_info)

    db.delete_device(dish1_dev_name)
    dish1_admin_dev_proxy.RestartServer()

    check_dish1_info = db.get_device_info("ska001/elt/master")
    LOGGER.info("check_dish1_info is: %s", check_dish1_info)


@when("command TelescopeStandBy is sent")
def invoke_telescope_standby_command():
    LOGGER.info("Invoke TelescopeStandBy command")
    centralnode_proxy.TelescopeStandBy()


@then("the Central Node is still running")
def check_if_central_node_running():
    """Method to check if central node is still running"""
    assert centralnode_proxy.ping() > 0


@then(parsers.parse("Dish with ID {test_dish_id} comes back"))
def connect_to_dish(test_dish_id):
    """Method to restablish the connection with the lost dish"""
    LOGGER.info("test_dish_id: %s", test_dish_id)

    # Add Dish device back to DB
    dev_info = DbDevInfo()
    dev_info.name = dish1_dev_name
    dev_info._class = dish1_dev_class
    dev_info.server = dish1_dev_server
    db.add_device(dev_info)

    dish1_admin_dev_proxy.RestartServer()

    check_dish1_info = db.get_device_info("ska001/elt/master")
    LOGGER.info("check_dish1_info is: %s", check_dish1_info)


@then("command TelescopeStandBy can be sent and received by the dish")
def move_telescope_to_stanby_state():
    LOGGER.info("Invoke TelescopeStandBy() with all real sub-systems")
    centralnode_proxy.TelescopeStandBy()


@then("the Central Node is still running")
def recheck_if_central_node_running(central_node_mid, event_recorder):
    assert centralnode_proxy.ping() > 0


@then("the telescope is in Standby state")
def check_if_telescope_is_in_stanby_state(event_recorder):
    dish1_info = db.get_device_info("ska001/elt/master")
    LOGGER.info("dish1_info is: %s", dish1_info)

    dish1_dev_name = dish1_info.ds_full_name
    LOGGER.info("dish1_dev_name is: %s", dish1_dev_name)

    dish1_proxy = DeviceProxy(dish1_dev_name)
    LOGGER.info("dish1_proxy is: %s", dish1_proxy)

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
    time.sleep(1)
    assert event_recorder.has_change_event_occurred(
        centralnode_proxy,
        "telescopeState",
        DevState.OFF,
    )
