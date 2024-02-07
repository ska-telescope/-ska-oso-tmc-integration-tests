@XTP- XXXXX @XTP-29778 @Team_SAHYADRI @tmc_dish
Scenario: TMC executes Scan command on DISH.LMC
    Given a Telescope consisting of TMC, DISH <dish_ids>, simulated CSP and simulated SDP
    And the Telescope is in ON state
    And TMC subarray <subarray_id> is in READY ObsState and DishMaster <dish_ids> is in pointingState TRACK
    When I issue the scan command to the TMC subarray <subarray_id>
    Then the DishMaster <dish_ids> transitions to dishMode OPERATE and pointingState SCAN  
    And TMC subarray node <subarray_id> obsState transitions to READY
    Examples:

        | subarray_id | dish_ids                           |
        | 1           | dish001,dish036,dish063,dish100    |