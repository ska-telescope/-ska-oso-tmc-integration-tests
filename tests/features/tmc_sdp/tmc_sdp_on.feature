@XTP-29230 @real_sdp
Scenario: Start up the telescope having TMC and SDP subsystems
    Given a Telescope consisting of TMC, SDP, simulated CSP and simulated Dish
    And telescope state is OFF
    When I start up the telescope
    Then the SDP must go to ON state
    And telescope state is ON