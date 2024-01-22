@tmc_csp
Scenario: TMC executes an Abort on CSP subarray
    Given the telescope is in ON state
    And the TMC subarray <subarray_id> and CSP subarray <subarray_id> is in ObsState <obsstate>
    When I issued the Abort command to the TMC subarray <subarray_id>
    Then the CSP subarray <subarray_id> transitions to ObsState ABORTED
    And the TMC subarray <subarray_id> transitions to ObsState ABORTED
    Examples:
    | subarray_id | obsstate |
    | 1           | IDLE     |
    | 1           | READY    |