Feature: Successfully execute a scan after a failed assign resources
    Scenario: Successfully execute a scan after a failed attempt to assign resources
        Given a subarray <subarray_id> with resources <resources_list> in obsState EMPTY
        When I issue the command AssignResources passing an invalid JSON script to the subarray <subarray_id>
        Then the subarray <subarray_id> returns an error message
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
        | 1            | "SKA001"       |


     Scenario: Successfully execute a scan after a successive failed attempt to assign resources
        Given a subarray <subarray_id> with resources <resources_list> in obsState EMPTY
        When I issue the command AssignResources passing an invalid JSON script to the subarray <subarray_id>
        Then the subarray <subarray_id> returns an error message
        When I issue the command AssignResources passing an invalid JSON script2 to the subarray <subarray_id>
        Then the subarray <subarray_id> returns an error message
        When I issue the command AssignResources passing an invalid JSON script3 to the subarray <subarray_id>
        Then the subarray <subarray_id> returns an error message
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
        | 1            | "SKA001"       |