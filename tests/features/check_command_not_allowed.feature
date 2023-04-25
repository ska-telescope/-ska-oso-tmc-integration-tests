Feature:  Invalid unexpected commands
    Scenario: Unexpected commands not allowed when TMC subarray is empty
        Given the TMC is in ON state and the subarray is in EMPTY obsstate
        When the command <unexpected_command> is invoked on the/that subarray
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
        When the command <unexpected_command> is invoked on the/that subarray
        Then the TMC should reject the <unexpected_command> with ResultCode.Rejected
        And TMC subarray remains in IDLE obsState
        And TMC executes the RealeaseResources command successfully
        Examples:
            | unexpected_command  |
            | Scan                |
            | End                 |


