Feature: TMC handles initialization scenarios of setting and verifying Dish ID - VCC map
    @XTP-30250 @XTP-28347 @Team_HIMALAYA
    Scenario: TMC is able to load last used Dish-VCC configuration before restart
        Given TMC with default version of dish vcc map
        When I issue the command LoadDishCfg on TMC with Dish-VCC configuration file
        Then TMC displays the current version of Dish-VCC configuration   
        When I restart the CentralNode, CspMasterLeafNode and DishLeafNode
        Then TMC should set version of Dish-VCC version used before restart
        And TMC should report Dish-VCC config set to true