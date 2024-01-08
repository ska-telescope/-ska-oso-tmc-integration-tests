@XTP-29398 @tmc_sdp
Scenario: Abort configuring SDP using TMC
    Given TMC and SDP subarray busy configuring
    When I command it to Abort
    Then the SDP subarray should go into an aborted state
    And the TMC subarray obsState transitions to ABORTED