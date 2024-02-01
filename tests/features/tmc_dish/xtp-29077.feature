@XTP-29077 @Team_SAHYADRI @tmc_dish
Scenario Outline: Mid TMC Central Node robustness test with disappearing DishLMC
    Given a Telescope consisting of TMC, DISH, CSP and SDP
    And dishes with Dish IDs <dish_ids> are registered on the TangoDB
    And dishleafnodes for dishes with IDs <dish_ids> are available
    And command TelescopeOn was sent and received by the dishes
    When communication with Dish ID 001 is lost
    And command TelescopeOff is sent
    Then the Central Node is still running
    And Dish with ID 001 comes back
    And command TelescopeOff can be sent and received by the dish
    And the Central Node is still running
    And the telescope is in OFF state

    Examples:
        | dish_ids            |
        | "001,036,063,100"   |

