@XTP-29354 @XTP-29778 @Team_SAHYADRI @tmc_dish
Scenario: Start up Telescope with TMC and DISH devices
    Given a Telescope consisting of  TMC, DISH , simulated CSP and simulated SDP
    When I start up the telescope
    Then DISH must go to STANDBY-FP mode
    And telescope state is ON