Scenario Outline: TMC behaviour during five point calibration scan.
    Given a TMC
    And a subarray configured for a calibration scan
    And the subarray is in READY obsState
    When I perform four partial configurations with json <partial_configuration_json> and scans
    Then the subarray executes the commands successfully and is in READY obsState

    Examples:
    | partial_configuration_json                                                                                    |
    | partial_configure_1,partial_configure_2,partial_configure_3,partial_configure_4       |
