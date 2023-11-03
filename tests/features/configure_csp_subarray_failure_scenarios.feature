Feature: TMC SubarrayNode handles the failure when the Configure command fails on CSP Subarray
    @XTP-28436
    Scenario Outline: TMC behavior when Csp Subarray Configure raises exception
        Given a TMC
        And the TMC assigns resources is succesfully executed
        And the TMC SubarrayNode <subarray_id> Configure is in progress
        And Sdp Subarray <subarray_id> completes Configure
        And Csp Subarray <subarray_id> returns to obsState IDLE
        And the TMC SubarrayNode <subarray_id> stucks in CONFIGURING
        When I issue the command End on SDP Subarray <subarray_id>
        Then Tmc SubarrayNode <subarray_id> transitions to obsState IDLE
        And the SDP subarray <subarray_id> transitions to obsState IDLE

        Examples:
        | subarray_id  |
        | 1            |


    