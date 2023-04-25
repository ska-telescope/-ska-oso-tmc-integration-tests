Feature:  Invalid unexpected commands
    Scenario: Unexpected commands not allowed when TMC subarray is empty
        Given the TMC is in ON state and the subarray is in EMPTY obsstate
        When the command <unexpected_command> is invoked on that subarray
        Then the TMC should reject the <unexpected_command> with ResultCode.Rejected
        And TMC subarray remains in EMPTY obsstate
        And TMC executes the AssignResources command successfully
        Examples:
            | unexpected_command   |
            | Configure            |
            | Scan                 |
            | End                  |

    Scenario: Unexpected commands not allowed when TMC subarray is idle
        Given the TMC is in ON state and the subarray is in IDLE
        When the command <unexpected_command> is invoked on that subarray
        Then the TMC should reject the <unexpected_command> with ResultCode.Rejected
        And TMC subarray remains in IDLE obsState
        And TMC executes the <permitted_command> command successfully
        Examples:
            | unexpected_command  | permitted_command  |
            | Scan                |   Configure        |   
            | Scan                |   ReleaseResources |

    Scenario: Unexpected commands not allowed when TMC busy in assigning the resources for a subarray
        Given the TMC is in ON state and the subarray is busy in assigning the resources
        When the command <unexpected_command> is invoked on the subarray
        Then the TMC should reject the <unexpected_command> with ResultCode.Rejected
        And TMC completes assigning the resources for that subarray, and executes the Configure command successfully 
        Examples:
            | unexpected_command  | 
            | AssignResources     |    


