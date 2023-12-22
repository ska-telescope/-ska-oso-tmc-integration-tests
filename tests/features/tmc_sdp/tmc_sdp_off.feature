@XTP-29231 @real_sdp
Scenario: Switch off the telescope having TMC and SDP subsystems 
    Given a Telescope consisting of TMC and SDP that is in ON State
    And  simulated CSP and Dish in ON States
    And telescope state is ON
    When I switch off the telescope
    Then the sdp must go to OFF State
    And telescope state is OFF