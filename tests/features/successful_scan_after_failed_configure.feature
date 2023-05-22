@XTP-20321
Feature: Successfully execute a scan after a failed configure
    Scenario: Successfully execute a scan after a failed attempt to configure
        Given a subarray <subarray_id> with resources <resources_list> in obsState IDLE
        When I issue the command Configure passing an invalid JSON script to the subarray <subarray_id>
        Then the subarray <subarray_id> returns an error message
        And the subarray <subarray_id> remains in obsState IDLE
        When I issue the command Configure passing a correct JSON script
        Then the subarray transitions to obsState READY
        When I issue the command Scan
        Then the subarray transitions to obsState SCANNING
        When I issue the command EndScan
        Then the subarray transitions to obsState READY
        And implements the teardown

        Examples:
            | subarray_id  | resources_list |
            | 1            | "SKA001"       |