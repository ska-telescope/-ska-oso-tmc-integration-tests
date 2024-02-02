@XTP-30208 @XTP-29778 @Team_SAHYADRI @tmc_dish
Scenario: TMC executes Abort command on DISH.LMC when TMC Subarray in Resourcing
    Given a Telescope consisting of  TMC, DISH <dish_ids> , simulated CSP and simulated SDP
    And the Telescope is in ON state
    And the TMC subarray <subarray_id> is busy in assigning
    When I issue the Abort command to the TMC subarray
    Then the DishMaster <dish_ids> transitions to dishMode OPERATE and pointingState READY
    And the TMC subarray transitions to ObsState ABORTED

        Examples:
        | subarray_id  | dish_ids                           |
        | 1            | dish001, dish036, dish063, dish100 |
