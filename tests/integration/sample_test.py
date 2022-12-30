import pytest, tango  


@pytest.mark.SKA_low
def test_sample():
    proxy = tango.DeviceProxy("ska_low/tm_central/central_node")
    result = proxy.ping()
    assert result > 1