Scenario Outline: Verify TelescopeHealthState as Failed
    Given csp master, sdp master and dish masters health state is OK 
    When <devices> health state is <Health_State> 
    Then the TMC telescope health state is <telescope_Health_State>
    Examples:
        | devices                       | Health_State               | telescope_Health_State |   
        | csp master                    | FAILED                     |   FAILED               |  
        | sdp master                    | FAILED                     |   FAILED               |
        | csp master,sdp master         | FAILED,FAILED              |   FAILED               |
        | dish master 1                 | FAILED                     |   FAILED               | 
        | dish master 2                 | FAILED                     |   FAILED               |   
        | dish master 1,dish master 2   | FAILED,FAILED              |   FAILED               |  
        | csp master,dish master 1      | FAILED,FAILED              |   FAILED               |
        | csp master,dish master 2      | FAILED,FAILED              |   FAILED               |
        | sdp master,dish master 1      | FAILED,FAILED              |   FAILED               |  
        | sdp master,dish master 2      | FAILED,FAILED              |   FAILED               |  


Scenario Outline: Verify TelescopeHealthState as Degraded
    Given csp master, sdp master and dish masters health state is OK 
    When <devices> health state is <Health_State> 
    Then the TMC telescope health state is <telescope_Health_State>
    Examples:
        | devices                       | Health_State        | telescope_Health_State |   
        | csp master                    | DEGRADED            |   DEGRADED             |  
        | sdp master                    | DEGRADED            |   DEGRADED             |
        | csp master,sdp master         | DEGRADED,DEGRADED   |   DEGRADED             |
        | dish master 1                 | DEGRADED            |   DEGRADED             | 
        | dish master 2                 | DEGRADED            |   DEGRADED             |   
        | dish master 1,dish master 2   | DEGRADED,DEGRADED   |   DEGRADED             |  
        | csp master,dish master 1      | DEGRADED,DEGRADED   |   DEGRADED             |
        | csp master,dish master 2      | DEGRADED,DEGRADED   |   DEGRADED             |
        | sdp master,dish master 1      | DEGRADED,DEGRADED   |   DEGRADED             |  
        | sdp master,dish master 2      | DEGRADED,DEGRADED   |   DEGRADED             |  

