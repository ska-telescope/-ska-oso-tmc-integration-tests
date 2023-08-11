Scenario Outline: Validate Subarray Health State is Failed or Degraded when dish device health state is failed or degraded
Given csp subarray, sdp subarray and dish masters health state is OK
When I issue the command Assign Resource on Subarray Node
AND  The <Dish_Master_Devices> health state is <Dish_Master_Health_States>
Then subarray health state is <Subarray_Health_State>
Examples:
    | Devices                                                 | Device_Health_State  | Subarray_Health_State |   
    | csp subarray                                            | FAILED               |  FAILED               |
    | sdp subarray                                            | FAILED               |  FAILED               |
    | csp subarray,sdp subarray                               | FAILED,FAILED        |  FAILED               | 
    | csp subarray,sdp subarray                               | DEGRADED,DEGRADED    |  DEGRADED             |