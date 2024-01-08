@XTP-29399 @tmc_sdp
Scenario: Abort scanning SDP using TMC
    Given TMC and SDP subarray busy scanning
    When I command it to Abort
    Then the SDP subarray should go into an aborted state
    And the TMC subarray obsState transitions to ABORTED