Feature: TMC SubarrayNode handles the failure when the incremental AssignResources command fails on CSP Subarray
    Scenario Outline: TMC behavior when CSP Subarray incremental AssignResources raises exception
        Given a TMC
        And AssignResources is executed successfully on SubarrayNode <subarray_id>
        Given the next TMC SubarrayNode <subarray_id> assign resources is in progress
        And Csp Subarray <subarray_id> returns to obsState IDLE
        And Sdp Subarray <subarray_id> completes assignResources
        When I issue the command ReleaseAllResources on SDP Subarray <subarray_id>
        Then the SDP subarray <subarray_id> transitions to obsState EMPTY
        And Tmc SubarrayNode <subarray_id> transitions to obsState EMPTY

        Examples:
        | subarray_id  |
        | 1            |