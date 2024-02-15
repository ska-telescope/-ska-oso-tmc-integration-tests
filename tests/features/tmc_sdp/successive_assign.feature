Feature: TMC SubarrayNode handles the exception when AssignResources command fails on SDP Subarray
        @XTP-29381 @tmc_sdp
        Scenario Outline: Validate second AssignResources command  after first successful AssignResources and ReleaseResources are executed
        Given a TMC and SDP
        And a subarray <subarray_id> in the IDLE obsState
        When I release all resources assigned to subarray <subarray_id>
        Then the SDP subarray <subarray_id> must be in EMPTY obsState
        And TMC subarray <subarray_id> obsState transitions to EMPTY
        Then AssignResources is executed with updated <input_json1> on SubarrayNode <subarray_id> successfully
        Examples:
        | subarray_id  | input_json1    |
        | 1            | assign_resources_mid  |
