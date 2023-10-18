Feature: TMC SubarrayNode handles the failure when the AssignResources command fails on CSP Subarray
    @XTP-28259
    Scenario Outline: TMC behavior when Csp Subarray AssignResources raises exception
        Given a TMC 
        And the TMC SubarrayNode <subarray_id> assign resources is in progress
        And Sdp Subarray <subarray_id> completes assignResources
        And Csp Subarray <subarray_id> returns to obsState EMPTY
        And the TMC SubarrayNode <subarray_id> stucks in RESOURCING
        When I issue the command ReleaseAllResources on SDP Subarray <subarray_id>
        Then the SDP subarray <subarray_id> transitions to obsState EMPTY
        And Tmc SubarrayNode <subarray_id> transitions to obsState EMPTY

        Examples:
        | subarray_id  |
        | 1            |