Scenario: TMC executes a Restart on SDP subarray when subarray completes abort
    Given the telescope is in ON state
    And TMC and SDP subarray <subarray_id> is in ABORTED ObsState
    When I command it to Restart 
    Then the SDP subarray <subarray_id> should go into an EMPTY obsstate
    And the TMC subarray <subarray_id> obsState transitions to EMPTY
    Examples:
    | subarray_id |
    | 1           |