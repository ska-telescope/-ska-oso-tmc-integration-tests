"""
This module is used for testing Alarm-Handler configurator API
with multiple files.
"""
import os

import httpx
import pytest

namespace = os.getenv("KUBE_NAMESPACE")

@pytest.mark.post_deployment
@pytest.mark.SKA_mid
def test_configure_alarms_with_multiple_files():
    """Test method to configure alarm rules using 
    multiple alarm rules files
    """
    for filename in os.listdir('/app/tests/data/alarm_rules/'):
        if filename.endswith('.txt'):
            with open(os.path.join('/app/tests/data/alarm_rules/', filename), "r") as file:
                response = httpx.post(
                    f"http://alarm-handler-configurator.{namespace}.svc.cluster."
                    + "local:8004/add-alarms?fqdn=alarm%2Fhandler%2F01",
                    files={"file": (filename, file, "text/plain")},
                    data={"fqdn": "alarm/handler/01"},
                )
    response_data = response.json()
    assert len(response_data["alarm_summary"]["tag"]) == 3
    assert response_data["alarm_summary"]["tag"] == [
        "centralnode_healthstate_degraded",
        "centralnode_telescopehealthstate_degraded",
        "subarraynode_obsstate_fault",
    ]
    error_message = f"error loading alarm=centralnode_telescopehealthstate_degraded , AlarmHandler::load_alarm(): alarm 'centralnode_telescopehealthstate_degraded' already exist"
    assert error_message in response_data["error"]
    tear_down_alarms(response_data["alarm_summary"]["tag"])

def tear_down_alarms(tags_to_remove):
    for tag in tags_to_remove:
        response = httpx.post(
        f"http://alarm-handler-configurator.{namespace}.svc.cluster."
        + f"local:8004/remove-alarm?tag={tag}&"
        + "alarmhandlerfqdn=alarm%2Fhandler%2F01",
        data={
            "tag": tag,
            "alarmhandlerfqdn": "alarm/handler/01",
        },
    )
    response_data = response.json()
    assert response_data["alarm_summary"] == None
