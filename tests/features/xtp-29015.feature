Feature: TMC SubarrayNode handles the failure when the Incremental AssignResources command fails on SDP Subarray
    @XTP-29015 @SKA_mid
    Scenario Outline: TMC behavior when Sdp Subarray is stuck in obsState RESOURCING after incremental AssignResources
        Given a TMC
        And AssignResources is executed with <input_json1> successfully on SubarrayNode <subarray_id>
        Given the next TMC SubarrayNode <subarray_id> AssignResources is in progress with <input_json2>

        When I issue the Abort command on TMC SubarrayNode <subarray_id>
        Then the CSP, SDP and TMC subarray <subarray_id> transitions to obsState ABORTED
        When I issue the Restart command on TMC SubarrayNode <subarray_id>
        Then the CSP, SDP and TMC subarray <subarray_id> transitions to obsState EMPTY
        Then AssignResources command is executed successfully on the Subarray <subarray_id>

        Examples:
        | subarray_id  | input_json1                      | input_json2                                |
        | 1            | assign_resources_mid  | assign_resources_mid |