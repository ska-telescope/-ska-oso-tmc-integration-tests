@XTP-29583 @XTP-29842 @Team_SAHYADRI @tmc_csp
Scenario: Abort scanning CSP using TMC
    Given the telescope is in ON state
    And the TMC subarray <subarray_id> and CSP subarray <subarray_id> are busy in scanning
    When I issued the Abort command to the TMC subarray
    Then the CSP subarray transitions to ObsState ABORTED
    And the TMC subarray transitions to ObsState ABORTED
    Examples:
    | subarray_id |
    | 1           |