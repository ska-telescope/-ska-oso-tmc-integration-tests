Feature:  Invalid unexpected jsons
    Scenario:   Invalid json rejected by TMC for Configure command
        Given the TMC is On
        And the subarray is in IDLE obsState
        When the command Configure is invoked with <invalid_json> input
        Then the TMC should reject the <invalid_json> with ResultCode.Rejected
        And TMC subarray remains in IDLE obsState
        And TMC successfully executes the Configure command for the subarray with a valid json

        Examples:
            | invalid_json                           |
            | config_id_key_missing                  |
            | fsp_id_key_missing                     |
            | frequency_slice_id_key_missing         |
            | integration_factor_key_missing         |
            | zoom_factor_key_missing                |
            | incorrect_fsp_id                       |
