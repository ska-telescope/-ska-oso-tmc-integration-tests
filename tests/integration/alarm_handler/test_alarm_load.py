import logging

import pytest
from tango import DeviceProxy

from tests.resources.test_support.common_utils.tmc_helpers import (
    tear_down_configured_alarms,
)

logger = logging.getLogger(__name__)


@pytest.mark.post_deployment
@pytest.mark.SKA_mid
def test_load_alarm():
    """A method to load tmc alarm for Alarm handler instance"""
    alarm_handler = DeviceProxy("alarm/handler/01")
    alarm_formula = (
        "tag=CentralNode_telescopehealthstate_degraded;formula="
        "(ska_mid/tm_central/central_node/telescopehealthState == 1);"
        "priority=log;group=none;message="
        '("alarm for central node telescopehealthstate degraded")'
    )
    alarm_handler.Load(alarm_formula)
    alarm_list = alarm_handler.alarmList
    assert alarm_list == ("centralnode_telescopehealthstate_degraded",)
    tear_down_configured_alarms(alarm_handler, alarm_list)
