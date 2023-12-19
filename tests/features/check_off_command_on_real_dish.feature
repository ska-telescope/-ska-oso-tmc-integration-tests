Scenario: ShutDown with TMC and DISH devices
    Given a Telescope consisting of TMC and DISH that is in ON state
    And simulated SDP and CSP in ON state
    And telescope state is ON
    When I switch off the telescope
    Then DISH must go to STANDBY-LP mode
    And telescope is OFF