Feature: TMC SubarrayNode handles the failure when the Incremental AssignResources command fails on CSP Subarray
    @XTP-29013 @SKA_mid
    Scenario Outline: TMC behavior when Csp Subarray is stuck in obsState RESOURCING after incremental AssignResources
        Given a TMC
        And AssignResources is executed successfully on SubarrayNode <subarray_id>
        Given the next TMC SubarrayNode <subarray_id> AssignResources is in progress
        And Sdp Subarray <subarray_id> completes assign resources and transitions to obsState IDLE
        And Csp Subarray <subarray_id> is stuck in obsState RESOURCING
        And the TMC SubarrayNode <subarray_id> stucks in RESOURCING
        When I issue the Abort command on TMC SubarrayNode <subarray_id>
        Then the CSP, SDP and TMC subarray <subarray_id> transitions to obsState ABORTED
        When I issue the Restart command on TMC SubarrayNode <subarray_id>
        Then the CSP, SDP and TMC subarray <subarray_id> transitions to obsState EMPTY
        Then AssignResources command is executed successfully on the Subarray <subarray_id>

        Examples:
        | subarray_id  |
        | 1            |