Scenario Outline: TMC behaviour during 5 point calibration scan.
    Given a TMC
    And a subarray configured for a calibration scan
    When I perform 4 partial configurations and scans
    Then the subarray executes the commands successfully
    And is in READY obsState
