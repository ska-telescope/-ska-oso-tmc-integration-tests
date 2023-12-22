@XTP-29259 @real_csp_mid
Scenario: Assign resources to CSP subarray using TMC
    Given the telescope is in ON state
    And TMC subarray <subarray_id> is in EMPTY ObsState
    When I assign resources with <receptors> to TMC subarray <subarray_id>
    Then CSP subarray <subarray_id> transitioned to ObsState IDLE
    And TMC subarray <subarray_id> transitioned to ObsState IDLE
    Examples:
    | subarray_id | receptors                              |
    | 1           | "SKA001", "SKA002", "SKA003", "SKA004" |