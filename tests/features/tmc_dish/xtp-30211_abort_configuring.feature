@XTP-30211 @XTP-29778 @Team_SAHYADRI @tmc_dish
Scenario: Abort configuring DISH.LMC using TMC
    Given a Telescope consisting of TMC, DISH, simulated CSP and simulated SDP
    And the Telescope is in ON state
    And the TMC subarray <subarray_id> is busy configuring and DishMaster <dish_ids> is in pointingState TRACK
    When I issue the Abort command to the TMC subarray 
    Then the DishMaster <dish_ids> transitions to dishMode OPERATE and pointingState READY  
    And the TMC subarray transitions to ObsState ABORTED

        Examples:
        | subarray_id  | dish_ids                           |
        | 1            | dish001, dish036, dish063, dish100 |

