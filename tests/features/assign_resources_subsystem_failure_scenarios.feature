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


    @XTP-28282
    Scenario Outline: TMC behavior when Csp Subarray is stuck in obsState RESOURCING
        Given a TMC 
        And the TMC SubarrayNode <subarray_id> assign resources is in progress
        And Sdp Subarray <subarray_id> completes assignResources
        And Csp Subarray <subarray_id> is stuck in obsState RESOURCING
        And the TMC SubarrayNode <subarray_id> stucks in RESOURCING
        When I issue the Abort command on TMC SubarrayNode <subarray_id>
        Then the SDP subarray <subarray_id> transitions to obsState ABORTED
        And the CSP subarray <subarray_id> transitions to obsState ABORTED
        And Tmc SubarrayNode <subarray_id> transitions to obsState ABORTED
        When I issue the Restart command on TMC SubarrayNode <subarray_id>
        Then the SDP subarray <subarray_id> transitions to obsState EMPTY
        And the CSP subarray <subarray_id> transitions to obsState EMPTY
        And Tmc SubarrayNode <subarray_id> transitions to obsState EMPTY

        Examples:
        | subarray_id  |
        | 1            |

    
    @XTP-28259
    Scenario Outline: TMC behavior when SDP Subarray AssignResources raises exception
        Given a TMC 
        And the TMC SubarrayNode <subarray_id> assign resources is in progress
        And Csp Subarray <subarray_id> completes assignResources
        And Sdp Subarray <subarray_id> returns to obsState EMPTY
        And the TMC SubarrayNode <subarray_id> stucks in RESOURCING
        When I issue the command ReleaseAllResources on CSP Subarray <subarray_id>
        Then the CSP subarray <subarray_id> transitions to obsState EMPTY
        And Tmc SubarrayNode <subarray_id> transitions to obsState EMPTY

        Examples:
        | subarray_id  |
        | 1            |


    @XTP-28282
    Scenario Outline: TMC behavior when Sdp Subarray is stuck in obsState RESOURCING
        Given a TMC 
        And the TMC SubarrayNode <subarray_id> assign resources is in progress
        And Csp Subarray <subarray_id> completes assignResources
        And Sdp Subarray <subarray_id> is stuck in obsState RESOURCING
        And the TMC SubarrayNode <subarray_id> stucks in RESOURCING
        When I issue the Abort command on TMC SubarrayNode <subarray_id>
        Then the SDP subarray <subarray_id> transitions to obsState ABORTED
        And the CSP subarray <subarray_id> transitions to obsState ABORTED
        And Tmc SubarrayNode <subarray_id> transitions to obsState ABORTED
        When I issue the Restart command on TMC SubarrayNode <subarray_id>
        Then the SDP subarray <subarray_id> transitions to obsState EMPTY
        And the CSP subarray <subarray_id> transitions to obsState EMPTY
        And Tmc SubarrayNode <subarray_id> transitions to obsState EMPTY

        Examples:
        | subarray_id  |
        | 1            |

    @XTP-28259
    Scenario Outline: TMC behavior when CSP and SDP Subarrays AssignResources raise exception
        Given a TMC 
        And the TMC SubarrayNode <subarray_id> assign resources is in progress
        When Csp Subarray <subarray_id> returns to obsState EMPTY
        And Sdp Subarray <subarray_id> returns to obsState EMPTY
        Then Tmc SubarrayNode <subarray_id> aggregates to obsState EMPTY

        Examples:
        | subarray_id  |
        | 1            |