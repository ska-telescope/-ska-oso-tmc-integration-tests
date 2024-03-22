Scenario: TMC generates delay values 
    Given the telescope is in ON state
    And TMC subarray is in obsState IDLE
    When I configure the TMC subarray
    Then CSP Subarray Leaf Node starts generating delay values with proper epoch
    When I end the observation
    Then CSP Subarray Leaf Node stops generating delay values
    When I configure the subarray
    Then CSP Subarray Leaf Node starts generating delay values with proper epoch