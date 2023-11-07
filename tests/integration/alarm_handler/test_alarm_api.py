"""
This module is used for testing Alarm-Handler configurator API.
"""
import logging
import os

import httpx
import pytest

namespace = os.getenv("KUBE_NAMESPACE")


def add_alarms_api(filename):
    """Test method for add alarms API"""
    # for debugging, it will get removed before merge
    logging.debug(
        f"http://alarm-handler-configurator.{namespace}.svc.cluster."
        + "local:8004/add-alarms?fqdn=alarm%2Fhandler%2F01"
    )
    with open(
        f"/app/tests/resources/tmc_alarm_rules/{filename}", "rb"
    ) as file:
        response = httpx.post(
            f"http://alarm-handler-configurator.{namespace}.svc.cluster."
            + "local:8004/add-alarms?fqdn=alarm%2Fhandler%2F01",
            files={"file": (filename, file, "text/plain")},
            data={"fqdn": "alarm/handler/01"},
        )
        response_data = response.json()
        assert len(response_data["alarm_summary"]["tag"]) == 2
        assert response_data["alarm_summary"]["tag"] == [
            "CentralNode_telescopehealthstate_degraded",
            "SubarrayNode_obsstate_fault",
        ]


def remove_alarm_api():
    """Test method for remove alarms API"""
    response = httpx.post(
        f"http://alarm-handler-configurator.{namespace}.svc.cluster."
        + "local:8004/remove-alarm?tag=test1&alarmhandlerfqdn=alarm"
        + "%2Fhandler%2F01",
        data={
            "tag": "SubarrayNode_obsstate_fault",
            "alarmhandlerfqdn": "alarm/handler/01",
        },
    )
    response_data = response.json()
    print(response_data)
    assert response_data["alarm_summary"]["tag"] != [
        "SubarrayNode_obsstate_fault"
    ]


def alarm_rule_validation(filename, missing_attribute):
    """Test method to verify validation against alarm rules"""
    with open(
        f"/app/tests/resources/tmc_alarm_rules/{filename}", "rb"
    ) as file:
        response = httpx.post(
            f"http://alarm-handler-configurator.{namespace}.svc.cluster."
            + "local:8004/add-alarms?fqdn=alarm%2Fhandler%2F01",
            files={"file": (filename, file, "text/plain")},
            data={"fqdn": "alarm/handler/01"},
        )
        response_data = response.json()
        assert (
            f"Missing {missing_attribute} property" in response_data["error"]
        )


@pytest.mark.alarm_test
@pytest.mark.post_deployment
@pytest.mark.SKA_mid
def test_configure_alarms():
    """test case to configure alarms for mid"""
    add_alarms_api("alarm_rules.txt")


@pytest.mark.alarm_test
@pytest.mark.post_deployment
@pytest.mark.SKA_mid
def test_remove_alarm():
    """test case to remove alarm for mid"""
    remove_alarm_api()


@pytest.mark.alarm_test
@pytest.mark.parametrize(
    "alarm_rule_file, missing_attribute",
    [
        ("missing_tag_attribute.txt", "tag"),
        ("missing_formula_attribute.txt", "formula"),
        ("missing_priority_attribute.txt", "priority"),
        ("missing_group_attribute.txt", "group"),
        ("missing_message_attribute.txt", "message"),
    ],
)
@pytest.mark.post_deployment
@pytest.mark.SKA_mid
def test_validate_attribute_properties(alarm_rule_file, missing_attribute):
    """test case to validate alarm attribute properties for mid"""
    alarm_rule_validation(alarm_rule_file, missing_attribute)
