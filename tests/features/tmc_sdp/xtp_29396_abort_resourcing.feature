@XTP-29396 @tmc_sdp
Scenario: Abort assigning using TMC
    Given TMC subarray <subarray_id> and SDP subarray <subarray_id> busy in assigning resources
    When I command it to Abort
    Then the SDP subarray <subarray_id> transitions to ObsState ABORTED
    And the TMC subarray <subarray_id> transitions to ObsState ABORTED
    Examples:
    | subarray_id |
    | 1           |
