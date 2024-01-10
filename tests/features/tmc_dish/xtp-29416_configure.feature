@XTP-29416 @Team_SAHYADRI @tmc_dish
Scenario: Configure the telescope having TMC and Dish Subsystems
    Given a Telescope consisting of TMC, DISH , simulated CSP and simulated SDP
    And the Telescope is in ON state
    And TMC subarray is in IDLE ObsState
    When I issue the Configure command to the TMC subarray <subarray_id>
    Then dishMode transitions to OPERATE obsState
    And pointingState transitions to TRACK 
    And TMC subarray <subarray_id> obsState transitions to READY obsState

        Examples:
        | subarray_id |
        | 1           |