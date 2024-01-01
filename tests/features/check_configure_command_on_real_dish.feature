Scenario: Configure the telescope having TMC and Dish Subsystems
    Given a Telescope consisting of TMC, DISH , simulated CSP and simulated SDP
    And the Telescope is in ON state
    And TMC subarray <subarray_id> is in IDLE ObsState
    When I issue the Configure command to the TMC subarray <subarray_id>
    Then Dish Mode is transitioned to OPERATE
    And Pointing State is transitioned to TRACK
    And TMC subarray <subarray_id> obsState transitions to READY

        Examples:
        | subarray_id |
        | 1           |