Feature: Commands with invalid json input
    Scenario: AssignResource command with invalid JSON is rejected by the TMC 
        Given the TMC is in ON state and the subarray is in EMPTY obsState
        When the command AssignResources is invoked with <invalid_json> input
        Then TMC should reject the AssignResources command
        And TMC subarray remains in EMPTY obsState
        And the command AssignResources is invoked with valid_json input
        Examples:
            | invalid_json                             |
            | invalid_assign_json_without_pb_id        |
            | invalid_assign_json_without_scan_type_id |
            | invalid_assign_json_without_channel_keys |
            | invalid_assign_json_without_receiptor_id |
            

