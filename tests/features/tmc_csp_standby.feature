Scenario: Standby the Telescope with real TMC and CSP devices
    Given a Telescope consisting of TMC, CSP, simulated DISH and simulated SDP devices
    And telescope is in ON state
    When I standby the telescope
    Then the CSP must go to standby state
    And telescope state is STANDBY