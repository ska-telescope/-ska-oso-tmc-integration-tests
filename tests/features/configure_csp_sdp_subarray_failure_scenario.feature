Feature: TMC SubarrayNode handles the failure when the Configure command fails on CSP and SDP Subarrays    
    @SKA_mid @XTP-28837
    Scenario Outline: TMC behavior when CSP and SDP Subarrays Configure raise exception
        Given a TMC
        And the TMC assigns resources is succesfully executed 
        And the TMC SubarrayNode <subarray_id> configure is in progress
        When Csp Subarray <subarray_id> returns to obsState IDLE
        And Sdp Subarray <subarray_id> returns to obsState IDLE
        Then Tmc SubarrayNode <subarray_id> aggregates to obsState IDLE

        Examples:
        | subarray_id  |
        | 1            |