import json
import time

import pytest
import tango

ASSIGN_JSON = {
    "interface": "https://schema.skao.int/ska-low-csp-assignresources/2.0",
    "common": {"subarray_id": 1},
    "lowcbf": {
        "resources": [
            {
                "device": "fsp_01",
                "shared": True,
                "fw_image": "pst",
                "fw_mode": "unused",
            },
            {
                "device": "p4_01",
                "shared": True,
                "fw_image": "p4.bin",
                "fw_mode": "p4",
            },
        ]
    },
}
CONFIGURE_JSON = {
    "interface": "https://schema.skao.int/ska-low-tmc-configure/3.0",
    "transaction_id": "txn-....-00001",
    "mccs": {
        "stations": [{"station_id": 1}, {"station_id": 2}],
        "subarray_beams": [
            {
                "subarray_beam_id": 1,
                "update_rate": 0.0,
                "logical_bands": [
                    {"start_channel": 80, "number_of_channels": 16},
                    {"start_channel": 384, "number_of_channels": 16},
                ],
                "apertures": [
                    {
                        "aperture_id": "AP001.01",
                        "weighting_key_ref": "aperture2",
                    },
                    {
                        "aperture_id": "AP001.02",
                        "weighting_key_ref": "aperture3",
                    },
                    {
                        "aperture_id": "AP002.01",
                        "weighting_key_ref": "aperture2",
                    },
                    {
                        "aperture_id": "AP002.02",
                        "weighting_key_ref": "aperture3",
                    },
                    {
                        "aperture_id": "AP003.01",
                        "weighting_key_ref": "aperture1",
                    },
                ],
                "sky_coordinates": {
                    "timestamp": "2021-10-23T12:34:56.789Z",
                    "reference_frame": "ICRS",
                    "c1": 180.0,
                    "c1_rate": 0.0,
                    "c2": 45.0,
                    "c2_rate": 0.0,
                },
                "target": {
                    "reference_frame": "HORIZON",
                    "target_name": "DriftScan",
                    "az": 180.0,
                    "el": 45.0,
                },
            }
        ],
    },
    "sdp": {
        "interface": "https://schema.skao.int/ska-sdp-configure/0.4",
        "scan_type": "science_A",
    },
    "csp": {
        "interface": "https://schema.skao.int/ska-low-csp-configurescan/0.0",
        "subarray": {"subarray_name": "science period 23"},
        "common": {
            "config_id": "sbi-mvp01-20200325-00001-science_A",
            "subarray_id": 1,
            "frequency_band": "low",
        },
        "lowcbf": {
            "stations": {
                "stns": [[1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1]],
                "stn_beams": [
                    {
                        "beam_id": 1,
                        "freq_ids": [400],
                        "delay_poly": "tango://delays.skao.int/low/stn-beam/1",
                    }
                ],
            },
            "vis": {
                "fsp": {"firmware": "vis", "fsp_ids": [1]},
                "stn_beams": [
                    {
                        "stn_beam_id": 1,
                        "host": [[0, "192.168.0.1"]],
                        "port": [[0, 9000, 1]],
                        "mac": [[0, "02-03-04-0a-0b-0c"]],
                        "integration_ms": 849,
                    }
                ],
            },
        },
    },
    "tmc": {"scan_duration": 10.0},
}


@pytest.mark.SKA_low
@pytest.mark.configure1
def test_csp_on():
    processor1 = tango.DeviceProxy("low-cbf/processor/0.0.0")
    processor1.serialnumber = "XFL14SLO1LIF"
    processor1.subscribetoallocator("low-cbf/allocator/0")
    processor1.register()
    csp_subarray = tango.DeviceProxy("low-csp/subarray/01")
    csp_master = tango.DeviceProxy("low-csp/control/0")
    csp_master.adminMode = 0
    csp_subarray.adminMode = 0
    csp_leaf_node = tango.DeviceProxy("ska_low/tm_leaf_node/csp_subarray01")
    csp_mln = tango.DeviceProxy("ska_low/tm_leaf_node/csp_master")
    time.sleep(10)
    csp_mln.On()
    csp_leaf_node.On()
    time.sleep(50)
    csp_leaf_node.AssignResources(json.dumps(ASSIGN_JSON))
    time.sleep(50)
    assert csp_subarray.obsState == 2
    csp_leaf_node.Configure(json.dumps(CONFIGURE_JSON))
    time.sleep(100)
    assert csp_subarray.obsState == 4
