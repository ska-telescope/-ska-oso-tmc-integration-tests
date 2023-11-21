Feature: TMC is able to handle the failure when load dish cfg command fails
    @XTP-28680
    Scenario Outline: TMC returns error message when non existent file is provided in configuration  
        Given a TMC
        And Telescope is in ON state 
        When I issue the command LoadDishCfg on TMC with non existent file <file_name> in configuration    
        Then TMC rejects the command with error <error_message>
        Examples:
        | file_name                         | error_message                                                                                                      |
        | invalid_file_name                 | No telescope model data with key instrument/dishid_vcc_configuration/invalid_file_name.json exists! |

    @XTP-28682
    Scenario Outline: TMC returns error when invalid dish id is provided in configuration
        Given a TMC
        And Telescope is in ON state
        When I issue the command LoadDishCfg on TMC with invalid <dish_id>
        Then TMC rejects the command with error <error_message>
        Examples:
        | dish_id  | error_message                           |
        | ABC001   | Invalid Dish id ABC001 provided in Json |

    @XTP-28683
    Scenario Outline: TMC returns error when duplicate vcc id is provided in configuration
        Given a TMC
        And Telescope is in ON state
        When I issue the command LoadDishCfg on TMC with duplicate vcc id in configuration
        Then TMC rejects the command with error due to Duplicate Vcc ids found in json

    @XTP-28679
    Scenario Outline: TMC handling exception from CSP Subarray  
        Given a TMC
        And Telescope is in ON state
        When I issue the command LoadDishCfg on TMC and CSP Controller raises an exception
        Then sysParam and sourceSysParam attributes remains unchanged on CSP Master Leaf Node
        And command returns with error message <error_message>
        Examples:
        | error_message |
        | Exception occurred, command failed. |