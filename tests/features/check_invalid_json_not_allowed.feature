Feature:  Invalid unexpected jsons
    Scenario:   Invalid json rejected by TMC for Configure command
        Given the TMC is On
        And the subarray is in IDLE obsState
        When the command Configure is invoked with <invalid_json> input
        Then the TMC should reject the <invalid_json> with ResultCode.Rejected
        And TMC subarray remains in IDLE obsState
        And TMC successfully executes the Configure command for the subarray with a valid json

        Examples:
            | invalid_json                                 |
            | command_Configure_missing_config_id          |
            | command_Configure_missing_fsp_id             |
            | command_Configure_incorrect_fsp_id           |
            | command_Configure_missing_frequency_slice_id |
            | command_Configure_missing_zoom_factor        |
            | command_Configure_missing_integration_factor |