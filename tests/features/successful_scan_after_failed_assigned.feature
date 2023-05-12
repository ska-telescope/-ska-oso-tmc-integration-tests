Feature: Successfully execute a scan after a failed assign resources
    Scenario: Successfully execute a scan after a failed attempt to assign resources
        Given a subarray with resources in obsState EMPTY
        When I issue the command AssignResources passing an invalid JSON script to the subarray 
        Then the subarray returns an error message
        And the subarray remains in obsState EMPTY 
        When I issue the command AssignResources passing a correct JSON script
        Then the subarray transitions to obsState IDLE
        When I issue the command Configure passing a correct JSON script  
        Then the subarray transitions to obsState READY
        When I issue the command Scan
        Then the subarray transitions to obsState SCANNING
        When I issue the command EndScan 
        Then the subarray transitions to obsState READY
        And the data is recorded as expected


     Scenario: Successfully execute a scan after a successive failed attempt to assign resources
        Given a subarray with resources in obsState EMPTY
        When I issue the command AssignResources passing an invalid JSON script to the subarray 
        Then the subarray returns an error message
        When I issue the command AssignResources passing an invalid JSON script to the subarray 
        Then the subarray returns an error message
        When I issue the command AssignResources passing an invalid JSON script to the subarray 
        Then the subarray returns an error message
        And the subarray remains in obsState EMPTY 
        When I issue the command AssignResources passing a correct JSON script
        Then the subarray transitions to obsState IDLE
        When I issue the command Configure passing a correct JSON script  
        Then the subarray transitions to obsState READY
        When I issue the command Scan
        Then the subarray transitions to obsState SCANNING
        When I issue the command EndScan 
        Then the subarray transitions to obsState READY
        And the data is recorded as expected