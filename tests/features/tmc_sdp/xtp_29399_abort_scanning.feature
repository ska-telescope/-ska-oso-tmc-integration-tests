@XTP-29399 @tmc_sdp
Scenario: Abort scanning SDP using TMC
    Given TMC subarray <subarray_id> and SDP subarray busy scanning
    When I command it to Abort
    Then the SDP subarray <subarray_id> transitions to ObsState ABORTED
    And the TMC subarray <subarray_id> transitions to ObsState ABORTED
    | subarray_id |
    | 1           |
