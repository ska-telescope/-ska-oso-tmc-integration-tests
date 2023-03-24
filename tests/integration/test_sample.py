import pytest, tango  
import os

@pytest.mark.TEST
def test_sample():
    os.environ["TANGO_HOST"] = "tango-databaseds:10000"
#    proxy = tango.DeviceProxy("mid-csp/control/0")
    proxy = tango.DeviceProxy("sim-csp/control/0")
    result = proxy.ping()
    assert result > 1
    # proxy.temperature = 30
    # proxy.windspeed = 50.0
    # proxy.ionization = 10
    # proxy.humidity = 20
    
    # proxy1 = tango.DeviceProxy("test/WeatherStation/1")
    # assert proxy1.temperature == 30
    # assert proxy1.windspeed == 50.0
    # assert proxy1.ionization == 10
    # assert proxy1.humidity == 20
    
"""Test to verify alarm-handler configuration"""

"""
Test Elettra Alarm Handler
"""

@pytest.mark.ALARM
def test_load_alarm():
  """ Test to load and verify the configured alarm. """
  alarm_device = tango.DeviceProxy("alarm/handler/01")
  # central_node = tango.DeviceProxy("ska_mid/tm_central/central_node")
  power_supply = tango.DeviceProxy("ps/power_supply/1")
  # weather_proxy.temperature = 50.0
  print(alarm_device.alarmSummary)
  # central_node.TelescopeOff()
  alarm_device.command_inout("Load","tag=powersupply;formula=(ps/power_supply/1/current > 20);priority=log;group=none;message=(\"alarm for current\")")
  tag="weather"
  searched_alarm = alarm_device.command_inout("SearchAlarm",tag)
  assert "test" in searched_alarm[0]
