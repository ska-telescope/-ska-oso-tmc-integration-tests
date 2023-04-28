Feature: Commands with invalid json input
    Scenario: AssignResource command with invalid JSON is rejected by the TMC 
        Given the TMC is in ON state and the subarray is in EMPTY obsState
        When the command assignresources is invoked for the subarray with <invalid_json> input
        Then the TMC should reject the AssignResources command with ResultCode.Rejected
        And TMC subarray remains in EMPTY obsState
        And TMC successfully executes the AssignResources command for the subarray with a valid json
        Examples:
            | invalid_json         |
            | invalid_assign_json1 |
            | invalid_assign_json2 |
            | invalid_assign_json3 |
            

