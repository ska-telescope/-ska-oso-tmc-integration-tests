Scenario Outline: TMC behaviour during a science scan after a five point calibration scan.
    Given a TMC
    And a subarray post five point calibration
    When I invoke Configure command for a science scan
    Then the subarray fetches calibration solutions from SDP and applies them to the Dishes
    And is in READY obsState
