Scenario Outline: TMC behaviour during five point calibration scan.
    Given a TMC
    And a subarray configured for a calibration scan
    And the subarray is in READY obsState
    When I perform four partial configurations with json <partial_configuration_json> and scans
    Then the subarray executes the commands successfully
    And is in READY obsState

    Example:
    | partial_configuration_json |
    | partial_configure_json_1,  partial_configure_json_2, partial_configure_json_3, partial_configure_json_4       |
