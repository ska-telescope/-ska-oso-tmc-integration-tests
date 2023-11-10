Feature: TMC is able to handle the failure when load dish cfg command fails
    Scenario Outline: TMC returns error message when non existent file is provided in configuration  
        Given a TMC
        AND Telescope is in ON state 
        When I issue the command LoadDishCfg on TMC with non existent file <file_name> in configuration    
        Then TMC rejects the command with error <error_message>
        Examples:
        | file_name                         | error_message                                                                                                      |
        | mid_cbf_initial_parameters_1.json | No telescope model data with key instrument/dishid_vcc_map_configuration/mid_cbf_initial_parameters_1.json exists! |        |


    Scenario Outline: TMC returns error when invalid dish id is provided in configuration
        Given a TMC
        AND Telescope is in ON state
        When I issue the command LoadDishCfg on TMC with invalid <dish_id>
        Then TMC rejects the command with error <error_message>
        Examples:
        | dish_id  | error_message                           |
        | ABC001   | Invalid Dish id ABC001 provided in Json |

    Scenario Outline: TMC returns error when duplicate vcc id is provided in configuration
        Given a TMC
        AND Telescope is in ON state
        When I issue the command LoadDishCfg on TMC with duplicate vcc id in configuration
        Then TMC rejects the command with error due to Duplicate Vcc ids found in json

    Scenario Outline: TMC handling exception from CSP Subarray  
        Given a TMC
        When I issue the command LoadDishCfg on TMC AND CSP Subarray raises an exception
        Then sysParam and sourceSysParam attributes remains unchanged on CSP Subarray Leaf Node
        AND command returns with error message <error_message>
        Examples:
        | error_message |
        | Exception occurred, command failed. |

        

