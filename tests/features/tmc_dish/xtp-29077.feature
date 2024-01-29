@XTP-29077 @Team_SAHYADRI @tmc_dish
Scenario Outline: Mid TMC Central Node robustness test with disappearing DishLMC
    Given dishes with Dish IDs <dish_ids> are registered on the TangoDB
    And a Telescope consisting of TMC, DISH , CSP and SDP
    And command TelescopeOn was sent and received by the dishes
    And dishleafnodes for dishes with IDs <dish_ids> are available
    When communication with Dish ID <test_dish_id> is lost
    And command TelescopeStandBy is sent
    Then the Central Node is still running
    And Dish with ID <test_dish_id> comes back
    And command TelescopeStandBy can be sent and received by the dish
    And the Central Node is still running
    And the telescope is in Standby state

    Examples:
        | dish_ids          | test_dish_id |
        | 001,036,063,100   | 001       |

