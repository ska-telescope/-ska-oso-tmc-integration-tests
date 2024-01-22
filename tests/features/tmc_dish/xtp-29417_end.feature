@XTP-29417 @XTP-29778 @Team_SAHYADRI @tmc_dish
Scenario: TMC executes End command on DISH.LMC
    Given a Telescope consisting of TMC, DISH , simulated CSP and simulated SDP
    And the Telescope is in ON state
    And TMC subarray <subarray_id> is in READY ObsState
    When I issue the End command to the TMC subarray <subarray_id>  
    Then dishMode transitions to STANDBY-FP obsState
    And pointingState transitions to READY
    And TMC subarray <subarray_id> obsState transitions to IDLE obsState

        Examples:
        | subarray_id |
        | 1           | 