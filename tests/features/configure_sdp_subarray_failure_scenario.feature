Feature: TMC SubarrayNode handles the failure when the Configure command fails on SDP Subarray    
    @XTP-28338
    Scenario Outline: TMC behavior when SDP Subarray Configure raises exception
        Given a TMC
        And the TMC assigns resources is succesfully executed
        And the TMC SubarrayNode <subarray_id> Configure is in progress
        And Csp Subarray <subarray_id> completes Configure
        And Sdp Subarray <subarray_id> returns to obsState IDLE
        And the TMC SubarrayNode <subarray_id> stucks in CONFIGURING
        When I issue the command End on CSP Subarray <subarray_id>
        Then the CSP subarray <subarray_id> transitions to obsState IDLE
        And Tmc SubarrayNode <subarray_id> transitions to obsState IDLE

        Examples:
        | subarray_id  |
        | 1            |


    Scenario Outline: TMC behavior when Sdp Subarray is stuck in obsState CONFIGURING
        Given a TMC
        And the TMC assigns resources is succesfully executed
        And the TMC SubarrayNode <subarray_id> Configure is in progress
        And Csp Subarray <subarray_id> completes Configure
        And Sdp Subarray <subarray_id> is stuck in obsState CONFIGURING
        And the TMC SubarrayNode <subarray_id> stucks in CONFIGURING
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