@XTP- @XTP-29778 @Team_SAHYADRI @tmc_dish
Scenario : TMC executes Scan command on DISH.LMC
    Given a Telescope consisting of TMC, DISH , simulated CSP and simulated SDP
    And the Telescope is in ON state
    And TMC subarray <subarray_id> is in READY ObsState
    When I issue the scan command to the TMC subarray <subarray_id>
    Then Dish Mode is transitioned to dish mode OPERATE
    And Pointing State is transitioned TRACK
    And TMC subarray node <subarray_id> obsState transitions to READY
    Examples:

        | subarray_id |
        | 1 |