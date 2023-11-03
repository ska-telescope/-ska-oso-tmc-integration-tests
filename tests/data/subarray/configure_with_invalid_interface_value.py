{
    "interface": "https://schema.skao.int/ska-tmc-configure/2.0",
    "transaction_id": "txn-....-00001",
    "pointing": {
        "target": {
            "reference_frame": "ICRS",
            "target_name": "Polaris Australis",
            "ra": "21:08:47.92",
            "dec": "-88:57:22.9",
        }
    },
    "dish": {"receiver_band": "2"},
    "csp": {
        "interface": "https://schema.skao.int/ska-csp-configure/2.0",
        "subarray": {"subarray_name": "science period 23"},
        "common": {
            "config_id": "sbi-mvp01-20200325-00001-science_A",
            "frequency_band": "1",
            "subarray_id": 1,
        },
        "cbf": {
            "fsp": [
                {
                    "fsp_id": 1,
                    "function_mode": "CORR",
                    "frequency_slice_id": 1,
                    "integration_factor": 1,
                    "zoom_factor": 0,
                    "channel_averaging_map": [[0, 2], [744, 0]],
                    "channel_offset": 0,
                    "output_link_map": [[0, 0], [200, 1]],
                },
                {
                    "fsp_id": 2,
                    "function_mode": "CORR",
                    "frequency_slice_id": 2,
                    "integration_factor": 1,
                    "zoom_factor": 1,
                    "channel_averaging_map": [[0, 2], [744, 0]],
                    "channel_offset": 744,
                    "output_link_map": [[0, 4], [200, 5]],
                    "zoom_window_tuning": 650000,
                },
            ],
            "vlbi": {},
        },
        "pss": {},
        "pst": {},
    },
    "sdp": {
        "interface": "https://schema.skao.int/ska-sdp-assign/0.3",
        "scan_type": "science_A",
    },
    "tmc": {"scan_duration": 10.0},
}
