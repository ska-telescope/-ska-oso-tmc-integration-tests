@XTP-30210 @XTP-29778 @Team_SAHYADRI @tmc_dish
Scenario: TMC executes Abort command on DISH.LMC when TMC Subarray is in READY
    Given a Telescope consisting of  TMC, DISH , simulated CSP and simulated SDP  
    And the Telescope is in ON state
    And the TMC subarray <subarray_id> is in READY ObsState and DISH.LMC is in pointingState TRACK
    When I issue the Abort command to the TMC subarray 
    Then the DISH transitions to dishMode OPERATE and pointingState READY
    And the TMC subarray transitions to ObsState ABORTED

        Examples:
        | subarray_id |
        | 1           |
