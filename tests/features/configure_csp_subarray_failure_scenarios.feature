Feature: TMC SubarrayNode handles the failure when the Configure command fails on CSP Subarray
    @SKA_mid @XTP-28436
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

    @SKA_mid @XTP-28834
    Scenario Outline: TMC behavior when Csp Subarray is stuck in obsState CONFIGURING
        Given a TMC
        And the TMC assigns resources is succesfully executed
        And the TMC SubarrayNode <subarray_id> Configure is in progress
        And Sdp Subarray <subarray_id> completes Configure
        And Csp Subarray <subarray_id> is stuck in obsState CONFIGURING
        And the TMC SubarrayNode <subarray_id> stucks in CONFIGURING
        When I issue the Abort command on TMC SubarrayNode <subarray_id>
        Then the SDP subarray <subarray_id> transitions to obsState ABORTED
        And the CSP subarray <subarray_id> transitions to obsState ABORTED
        And Tmc SubarrayNode <subarray_id> transitions to obsState ABORTED
        When I issue the Restart command on TMC SubarrayNode <subarray_id>
        Then the SDP subarray <subarray_id> transitions to obsState EMPTY
        And the CSP subarray <subarray_id> transitions to obsState EMPTY
        And Tmc SubarrayNode <subarray_id> transitions to obsState EMPTY
        And Configure command is executed successfully on the Subarray <subarray_id>

        Examples:
        | subarray_id  |
        | 1            |


    