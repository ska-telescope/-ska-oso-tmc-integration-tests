@XTP-29396 @tmc_sdp
Scenario: Abort assigning using TMC
    Given TMC and SDP subarray busy assigning resources
    When I command it to Abort
    Then the SDP subarray should go into an ABORTED obsstate
    And the TMC subarray obsState transitions to ABORTED




