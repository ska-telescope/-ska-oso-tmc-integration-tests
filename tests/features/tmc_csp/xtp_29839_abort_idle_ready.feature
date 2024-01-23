@XTP-29583 @XTP-29839 @Team_SAHYADRI @tmc_csp
Scenario: TMC executes an Abort on CSP subarray
    Given the telescope is in ON state
    And the TMC subarray <subarray_id> and CSP subarray <subarray_id> are in ObsState <obsstate>
    When I issued the Abort command to the TMC subarray
    Then the CSP subarray transitions to ObsState ABORTED
    And the TMC subarray transitions to ObsState ABORTED
    Examples:
        | subarray_id | obsstate |
        | 1           | IDLE     |
        | 1           | READY    |