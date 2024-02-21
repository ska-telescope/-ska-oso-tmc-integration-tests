Feature:  TMC executes successive configure commands with real sdp devices
    Scenario: TMC validates reconfigure functionality with real sdp devices
        Given a TMC and SDP
        And a subarray <subarray_id> in the IDLE obsState
        When the command configure is issued with <input_json1>
        And the subarray transitions to obsState READY
        And the next successive configure command is issued with <input_json2>
        Then the subarray reconfigures changing its obsState to READY

        Examples:
            | subarray_id  | input_json1           |      input_json2       |
            | 1  | sdp_mid_configure1   |   sdp_mid_configure2  |
            | 1  | sdp_mid_configure1   |   sdp_mid_configure1  |



