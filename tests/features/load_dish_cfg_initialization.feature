Feature: TMC is able to load Dish-VCC map configuration during initialization of CentralNode and CspMasterLeaf Node
    Scenario Outline: TMC is able to load Dish-VCC configuration file during initialization of CspMasterLeafNode
        Given TMC with default version of dish vcc map
        When I restart the CspMasterLeafNode and CentralNode is running   
        Then CSP Master Leaf Node should able to load Dish-VCC version set before restart 
        And TMC should report Dish-VCC config set to true
    
    Scenario Outline: TMC is able to load last used Dish-VCC configuration before restart 
        Given TMC with default version of dish vcc map
        When I issue the command LoadDishCfg on TMC with Dish-VCC configuration file
        Then TMC displays the current version of Dish-VCC configuration   
        When I restart the CentralNode and CspMasterLeafNode
        Then TMC should set version of Dish-VCC version used before restart
    
    Scenario Outline: TMC is able to load Dish-VCC configuration file during initialization of CentralNode
        Given TMC with default version of dish vcc map
        When I restart the CentralNode and CspMasterLeafNode is running   
        Then TMC should set Dish-VCC config set to True after restart

    Scenario Outline: TMC should report Dish-VCC config set as False when Dish-VCC Config is mismatch
        Given TMC with default version of dish vcc map
        When I make Dish-VCC version on CSP Master Leaf Node empty and Restart CSPMasterLeafNode   
        Then TMC should set Dish-VCC config set to False after Restart
        And TMC should report that Dish-VCC version mismatch between CSPMasterLeafNode and CSPMaster