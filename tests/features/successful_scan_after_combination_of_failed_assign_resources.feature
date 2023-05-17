Scenario: Successfully execute a scan after combination of failed assign resources
    Given a subarray <subarray_id> with resources <resources_list> in obsState EMPTY
    When I issue the command AssignResources with unavailable resources <resources_list> to the subarray <subarray_id>
    Then the subarray <subarray_id> returns an error message two
    When I issue the command AssignResources passing an invalid JSON script to the subarray <subarray_id>
    Then the subarray <subarray_id> returns an error message one
    And the subarray <subarray_id> remains in obsState EMPTY
    When I issue the command AssignResources passing a correct JSON script
    Then the subarray transitions to obsState IDLE
    When I issue the command Configure passing a correct JSON script  
    Then the subarray transitions to obsState READY
    When I issue the command Scan
    Then the subarray transitions to obsState SCANNING
    When I issue the command EndScan 
    Then the subarray transitions to obsState READY
    And implements the teardown
    Examples:
    | subarray_id  | resources_list |
    | 1            | "SKA999"       |


Scenario: Successfully execute a scan after second combination of failed assign resources
    Given a subarray <subarray_id> with resources <resources_list> in obsState EMPTY
    When I issue the command AssignResources passing an invalid JSON script to the subarray <subarray_id>
    Then the subarray <subarray_id> returns an error message one
    When I issue the command AssignResources with unavailable resources <resources_list> to the subarray <subarray_id>
    Then the subarray <subarray_id> returns an error message two
    And the subarray <subarray_id> remains in obsState EMPTY
    When I issue the command AssignResources passing a correct JSON script
    Then the subarray transitions to obsState IDLE
    When I issue the command Configure passing a correct JSON script  
    Then the subarray transitions to obsState READY
    When I issue the command Scan
    Then the subarray transitions to obsState SCANNING
    When I issue the command EndScan 
    Then the subarray transitions to obsState READY
    And implements the teardown
    Examples:
    | subarray_id  | resources_list |
    | 1            | "SKA999"       |