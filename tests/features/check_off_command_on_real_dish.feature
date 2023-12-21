Scenario: ShutDown with TMC and DISH devices
    Given a Telescope consisting of TMC, DISH, simulated CSP and simulated SDP is in ON state
    When I switch off the telescope
    Then DISH must go to STANDBY-LP mode
    And telescope is OFF