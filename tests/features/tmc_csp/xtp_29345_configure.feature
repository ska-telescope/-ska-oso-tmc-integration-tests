@XTP-29345 @tmc_csp
Scenario Outline: Configure a CSP subarray for a scan using TMC
    Given the telescope is in ON state
    And TMC subarray <subarray_id> in ObsState IDLE
    When I issue the Configure command to the TMC subarray <subarray_id>
    Then the CSP subarray  <subarray_id> transitions to ObsState READY
    And the TMC subarray <subarray_id> transitions to ObsState READY
    And CSP subarray leaf node <subarray_id> starts generating delay values
    And delay model json is validated against it's json schema
    Examples:
    | subarray_id |
    | 1           |