Feature: TMC able to load Dish and VCC map configuration file and display current version of file
    Scenario Outline: TMC able to load Dish and VCC configuration file  
        Given a TMC 
        When I issue the command LoadDishCfg on TMC with Dish and VCC configuration file   
        Then TMC should pass the configuration to CSP Controller
        AND TMC should set Dish k-numbers provided in file on dish masters
        AND TMC display current version of Dish and VCC configuration 
  