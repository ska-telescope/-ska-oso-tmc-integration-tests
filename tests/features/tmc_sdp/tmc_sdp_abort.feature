Scenario: Abort assigning using TMC
    Given TMC and SDP subarray busy assigning resources
    When I command it to Abort
    Then the SDP subarray should go into an ABORTED obsstate
    And the TMC subarray obsState transitions to ABORTED

Scenario: TMC executes an Abort on SDP subarray while subarray completes configuration
    Given the telescope is in ON state
    And TMC and SDP subarray is in <obsstate> ObsState
    When I issued the Abort command to the TMC subarray <subarray_id>
    Then the SDP subarray should go into an ABORTED ObsState
    And the TMC subarray <subarray_id> transitions to ABORTED ObsState
    Examples:
    | subarray_id | obsstate |
    | 1           | IDLE     |


