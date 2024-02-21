Feature: TMC Subarray handles the exception when AssignResources command fails on SDP Subarray
    @XTP-29381 @tmc_sdp
    Scenario Outline: TMC Subarray handles the exception duplicate eb-id raised by SDP subarray

        Given The TMC and SDP subarray <subarray_id> in the IDLE obsState using <input_json1>
        When TMC executes second AssignResources command with duplicate eb-id from <input_json1>
        And SDP subarray <subarray_id> throws an exception and remain in IDLE obsState
        Then exception is propagated to central node
        And I issue the Abort command on TMC Subarray <subarray_id>
        And the CSP, SDP and TMC Subarray <subarray_id> transitions to obsState ABORTED
        And I issue the Restart command on TMC Subarray <subarray_id>
        And the CSP, SDP and TMC Subarray <subarray_id> transitions to obsState EMPTY
        Then AssignResources command is executed and TMC and SDP subarray <subarray_id> transitions to IDLE
        Examples:
        | subarray_id  | input_json1   |                                                 |
        | 1            | assign_resources_mid |