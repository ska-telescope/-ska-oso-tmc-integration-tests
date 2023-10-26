Feature: TMC SubarrayNode handles the failure when the AssignResources command fails on CSP and SDP Subarrays    
    @XTP-28340
    Scenario Outline: TMC behavior when CSP and SDP Subarrays AssignResources raise exception
        Given a TMC 
        And the TMC SubarrayNode <subarray_id> assign resources is in progress
        When Csp Subarray <subarray_id> returns to obsState EMPTY
        And Sdp Subarray <subarray_id> returns to obsState EMPTY
        Then Tmc SubarrayNode <subarray_id> aggregates to obsState EMPTY

        Examples:
        | subarray_id  |
        | 1            |