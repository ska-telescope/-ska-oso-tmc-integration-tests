Scenario Outline: Subarray Health State should be Failed or Degraded when one or more devices health state is Failed or Degraded
Given csp subarray, sdp subarray and dish masters health state is OK 
When The <Devices> health state changes to <Device_Health_State> 
Then subarray health state is <Subarray_Health_State>
Examples:
    | Devices                                                 | Device_Health_State  | Subarray_Health_State |   
    | csp subarray                                            | FAILED               |  FAILED               |
    | sdp subarray                                            | FAILED               |  FAILED               |
    | csp subarray,sdp subarray                               | FAILED,FAILED        |  FAILED               | 
    | csp subarray,sdp subarray                               | DEGRADED,DEGRADED    |  DEGRADED             |
    | csp subarray,sdp subarray                               | DEGRADED,FAILED      |  FAILED               |
