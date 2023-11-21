Feature:  TMC executes Abort Command.
    Scenario: TMC validates Abort Command
    Given a Subarray in <obs_state> obsState
    When I Abort it
    Then the Subarray transitions to ABORTED obsState

Examples:
| obs_state   |
| IDLE        |