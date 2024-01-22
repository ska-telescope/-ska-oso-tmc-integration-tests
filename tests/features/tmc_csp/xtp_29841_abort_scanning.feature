@XTP-29583 @XTP-29841 @Team_SAHYADRI @tmc_csp
Scenario: Abort scanning CSP using TMC
    Given the telescope is in ON state
    And the TMC subarray <subarray_id> and CSP subarray <subarray_id> is busy in scanning
    When I issued the Abort command to the TMC subarray <subarray_id>
    Then the CSP subarray <subarray_id> transitions to ObsState ABORTED
    And the TMC subarray <subarray_id> transitions to ObsState ABORTED
    Examples:
    | subarray_id |
    | 1           |