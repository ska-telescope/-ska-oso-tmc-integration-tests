Feature: TMC SubarrayNode handles the failure when the incremental AssignResources command fails on CSP Subarray
    Scenario Outline: TMC behavior when CSP Subarray incremental AssignResources raises exception
        Given a TMC
        And AssignResources is executed successfully on SubarrayNode <subarray_id>
        Given the next TMC SubarrayNode <subarray_id> assign resources is in progress
        And Sdp and Csp Subarray <subarray_id> returns to obsState IDLE
        When I issue the command ReleaseAllResources on SDP Subarray <subarray_id>
        Then the SDP subarray <subarray_id> transitions to obsState EMPTY
        And Tmc SubarrayNode <subarray_id> transitions to obsState EMPTY

        Examples:
        | subarray_id  |
        | 1            |

    Scenario Outline: TMC behavior when Csp Subarray is stuck in obsState RESOURCING after incremental AssignResources
        Given a TMC
        And AssignResources is executed successfully on SubarrayNode <subarray_id>
        Given the next TMC SubarrayNode <subarray_id> AssignResources is in progress
        And Sdp Subarray <subarray_id> completes AssignResources
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