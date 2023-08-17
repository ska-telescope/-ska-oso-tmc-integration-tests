# TODO: Tests WIP
Scenario Outline: TMC behavior with invalid json data
    Given a TMC 
    And the Resources are assigned to TMC SubarrayNode
    When the TMC SubarrayNode is Configured with invalid json data
    Then the TMC SubarrayNode stuck in obsState CONFIGURING
    And Csp Subarray, Sdp Subarray remains in obsState IDLE


Scenario Outline: TMC behavior when Dish master raises exception
    Given a TMC 
    And the Resources are assigned to TMC SubarrayNode
    When the TMC SubarrayNode is Configured with json data
    Then Dish Master raises exception
    And Dish Master remains in pointingState SLEW
    And the TMC SubarrayNode stuck in obsState CONFIGURING


Scenario Outline: TMC behavior when Csp Subarray raises exception
    Given a TMC 
    And the Resources are assigned to TMC SubarrayNode
    When the TMC SubarrayNode is Configured with json data
    Then Csp Subarray raises exception
    And Csp Subarray remains in obsState CONFIGURING
    And the TMC SubarrayNode stuck in obsState CONFIGURING


Scenario Outline: TMC behavior when Sdp Subarray raises exception
    Given a TMC 
    And the Resources are assigned to TMC SubarrayNode
    When the TMC SubarrayNode is Configured with json data
    Then Sdp Subarray raises exception
    And Sdp Subarray remains in obsState CONFIGURING
    And the TMC SubarrayNode stuck in obsState CONFIGURING
