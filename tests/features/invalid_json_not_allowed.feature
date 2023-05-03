Feature: Commands with invalid json input
    Scenario: AssignResource command with invalid JSON is rejected by the TMC 
        Given the TMC is in ON state 
        And the subarray is in EMPTY obsState
        When the command AssignResources is invoked with <invalid_json> input
        Then TMC should reject the AssignResources command
        And TMC subarray remains in EMPTY obsState
        And the command AssignResources is invoked with valid_json input
        Examples:
            | invalid_json      |
            | pb_id             |
            | scan_type_id      |
            | count             |
            | receptor_id       |

            

