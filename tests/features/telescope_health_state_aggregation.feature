Scenario Outline: Verify TelescopeHealthState as Failed
    Given csp master, sdp master and dish masters health state is OK 
    When <devices> health state is <Health_State> 
    Then the TMC telescope health state is <telescope_Health_State>
    Examples:
        | devices                       | Health_State               | telescope_Health_State |   
        | csp master                    | FAILED                     |   FAILED               |  
        | sdp master                    | FAILED                     |   FAILED               |
        | csp master,sdp master         | FAILED,FAILED              |   FAILED               |
        | Dish master 1                 | FAILED                     |   FAILED               | 
        | Dish master 2                 | FAILED                     |   FAILED               |   
        | Dish master 1,Dish master 2   | FAILED,FAILED              |   FAILED               |  
        | csp master,Dish master 1      | FAILED,FAILED              |   FAILED               |
        | csp master,Dish master 2      | FAILED,FAILED              |   FAILED               |
        | sdp master,Dish master 1      | FAILED,FAILED              |   FAILED               |  
        | sdp master,Dish master 2      | FAILED,FAILED              |   FAILED               |  

