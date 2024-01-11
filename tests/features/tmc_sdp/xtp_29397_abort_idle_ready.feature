@XTP-29397 @tmc_sdp
Scenario: TMC executes an Abort on SDP subarray while subarray completes configuration
    Given the telescope is in ON state
    And TMC and SDP subarray <subarray_id> is in <obsstate> ObsState
    When I issued the Abort command to the TMC subarray <subarray_id>
    Then the SDP subarray <subarray_id> transitions to ObsState ABORTED
    And the TMC subarray <subarray_id> transitions to ObsState ABORTED
    Examples:
    | subarray_id | obsstate |
    | 1           | IDLE     |
    | 1           | READY    |