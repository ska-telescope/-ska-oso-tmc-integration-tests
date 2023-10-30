Feature: TMC SubarrayNode handles the failure when the incremental AssignResources command fails on SDP Subarray
    Scenario Outline: TMC behavior when SDP Subarray incremental AssignResources raises exception
        Given a TMC
        And the TMC SubarrayNode <subarray_id> assignResources is in progress with <input_json1>
        And Subarray completes assignResources
        Given the next TMC SubarrayNode <subarray_id> AssignResources is in progress with <input_json2>
        And Sdp Subarray <subarray_id> returns to obsState IDLE
        And Csp Subarray <subarray_id> completes assignResources
        When I issue the command ReleaseAllResources on CSP Subarray <subarray_id>
        Then the CSP subarray <subarray_id> transitions to obsState EMPTY
        And Tmc SubarrayNode <subarray_id> transitions to obsState EMPTY

        Examples:
        | subarray_id  | input_json1                      | input_json2                                |
        | 1            | incremental_assign_resources_01  | assign_resources_mid_invalid_sdp_resources |

    Scenario Outline: TMC behavior when Sdp Subarray is stuck in obsState RESOURCING after incremental AssignResources
        Given a TMC
        And the TMC SubarrayNode <subarray_id> AssignResources is in progress with <input_json1>
        And Subarray completes AssignResources
        Given the next TMC SubarrayNode <subarray_id> AssignResources is in progress with <input_json2>
        And Csp Subarray <subarray_id> completes AssignResources
        And Sdp Subarray <subarray_id> is stuck in obsState RESOURCING
        And the TMC SubarrayNode <subarray_id> stuck in RESOURCING
        When I issue the Abort command on TMC SubarrayNode <subarray_id>
        Then the SDP subarray <subarray_id> transitions to obsState ABORTED
        And the CSP subarray <subarray_id> transitions to obsState ABORTED
        And Tmc SubarrayNode <subarray_id> transitions to obsState ABORTED
        When I issue the Restart command on TMC SubarrayNode <subarray_id>
        Then the SDP subarray <subarray_id> transitions to obsState EMPTY
        And the CSP subarray <subarray_id> transitions to obsState EMPTY
        And Tmc SubarrayNode <subarray_id> transitions to obsState EMPTY

        Examples:
        | subarray_id  | input_json1                      | input_json2                                |
        | 1            | incremental_assign_resources_01  | assign_resources_mid_invalid_eb_id         |