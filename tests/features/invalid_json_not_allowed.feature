Feature: Commands with invalid json input
    Scenario: AssignResource command with invalid JSON is rejected by the TMC 
        Given the TMC is in ON state 
        And the subarray is in EMPTY obsState
        When the command AssignResources is invoked with <invalid_json> input
        Then TMC should reject the AssignResources command
        And TMC subarray remains in EMPTY obsState
        And TMC successfully executes AssignResources for subarray with a valid input json
        Examples:
            | invalid_json                  |
            | missing_pb_id_key             |
            | missing_scan_type_id_key      |
            | missing_count_key             |
            | missing_receptor_id_key       |

            

