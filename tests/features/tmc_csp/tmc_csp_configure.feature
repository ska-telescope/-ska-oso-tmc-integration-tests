Scenario: Configure a CSP subarray for a scan using TMC
    Given the telescope is in ON state
    And TMC subarray in ObsState IDLE
    When I issue the Configure command to the TMC subarray 1
    Then the CSP subarray 1 transitions to ObsState READY
    And the TMC subarray 1 transitions to ObsState READY
    And CSP subarray leaf node 1 starts generating delay values