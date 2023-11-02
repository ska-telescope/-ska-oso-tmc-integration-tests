Feature: TMC SubarrayNode handles the failure when the AssignResources command fails on CSP and SDP Subarrays
    Scenario Outline: TMC behavior when CSP and SDP Subarrays incremental AssignResources raise exception
        Given a TMC
        And AssignResources is executed successfully on SubarrayNode <subarray_id> with <input_json1>
        Given the next TMC SubarrayNode <subarray_id> AssignResources is in progress with <input_json2>
        When Csp Subarray <subarray_id> returns to obsState IDLE
        And Sdp Subarray <subarray_id> returns to obsState IDLE
        When I issue the command ReleaseAllResources on SDP Subarray <subarray_id>
        Then Tmc SubarrayNode <subarray_id> transitions to obsState EMPTY

       Examples:
       | subarray_id  | input_json1                      | input_json2                                |
       | 1            | incremental_assign_resources_01  | incremental_assign_resources_02            |