@XTP-29249 @real_csp_mid
Scenario: StartUp Telescope with TMC and CSP devices
    Given a Telescope consisting of TMC, CSP, simulated DISH and simulated SDP devices
    And telescope state is OFF
    When I start up the telescope
    Then the CSP must go to ON state
    And telescope state is ON