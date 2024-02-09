@XTP-29351 @XTP-29778 @Team_SAHYADRI @tmc_dish 
Scenario: Shut down with TMC and DISH devices
    Given a Telescope consisting of TMC, DISH <dish_ids>, simulated CSP and simulated SDP
    When I switch off the telescope
    Then DishMaster <dish_ids> must transition to STANDBY-LP mode
    And telescope is OFF

         Examples:
        | dish_ids                           |
        | dish001,dish036,dish063,dish100    |