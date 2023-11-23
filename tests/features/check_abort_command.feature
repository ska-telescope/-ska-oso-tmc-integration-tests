@XTP-28864
Scenario: TMC validates Abort Command
    Given a Subarray in <obs_state> obsState
    When I Abort it
    Then the Subarray transitions to ABORTED obsState

Examples:
| obs_state   |
| RESOURCING  |
| IDLE        |
| READY       |
| SCANNING    |
| CONFIGURING |

@XTP-28865
Scenario: TMC executes Abort Command in EMPTY obsState.
    Given a Subarray in EMPTY obsState
    When I Abort it
    Then TMC should reject the command with ResultCode.REJECTED
    And the Subarray remains in obsState EMPTY