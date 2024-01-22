@XTP-29583 @XTP-29840 @Team_SAHYADRI @tmc_csp
Scenario: Abort assigning CSP using TMC
    Given the telescope is in ON state
    And the TMC subarray <subarray_id> and CSP subarray <subarray_id> is busy in assigning
    When I issued the Abort command to the TMC subarray <subarray_id>
    Then the CSP subarray <subarray_id> transitions to ObsState ABORTED
    And the TMC subarray <subarray_id> transitions to ObsState ABORTED
    Examples:
    | subarray_id |
    | 1           |