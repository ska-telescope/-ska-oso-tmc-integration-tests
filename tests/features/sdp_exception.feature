Feature: TMC SubarrayNode handles the exception when AssignResources command fails on SDP Subarray
    @XTP-29381 @tmc_sdp
    Scenario Outline: TMC SubarrayNode handles the exception raised by SDP subarray and propagates to LRCR of centralnode
        Given a TMC
        And AssignResources is executed with <input_json1> successfully on SubarrayNode <subarray_id>
        And the next TMC SubarrayNode <subarray_id> AssignResources is executed with same eb-id <input_json1>
        Then SDP {subarray_id} throws exception and remain in IDLE status
        Then exception is propagated to central node
        Then I issue the Abort command on TMC SubarrayNode <subarray_id>
        Then the CSP, SDP and TMC subarray <subarray_id> transitions to obsState ABORTED
        When I issue the Restart command on TMC SubarrayNode <subarray_id>
        Then the CSP, SDP and TMC subarray <subarray_id> transitions to obsState EMPTY
        Then AssignResources command is executed successfully on the Subarray <subarray_id>

        Examples:
        | subarray_id  | input_json1   |                                                 |
        | 1            | assign_resources_mid |