Scenario: TMC generates delay values 
    Given the telescope is in ON state
    And TMC subarray <subarray_id> in ObsState IDLE
    When I configure the TMC subarray
    Then CSP Subarray Leaf Node starts generating delay values with proper epoch
    When I end the observation
    Then CSP Subarray Leaf Node stops generating delay values
    When I configure the TMC subarray
    Then CSP Subarray Leaf Node starts generating delay values with proper epoch
    Examples:
        | subarray_id |
        | 1           |