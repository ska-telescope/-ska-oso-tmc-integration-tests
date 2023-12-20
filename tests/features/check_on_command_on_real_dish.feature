Scenario: StartUp Telescope with TMC and DISH devices
    Given a Telescope consisting of  TMC, DISH , simulated CSP and simulated SDP
    When I start up the telescope
    Then DISH must go to STANDBY-FP mode
    And telescope state is ON


