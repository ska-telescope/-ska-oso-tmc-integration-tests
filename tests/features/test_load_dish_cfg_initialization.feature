Feature: TMC is able to load Dish and VCC map configuration during initialization of Central Node and CSP Master Leaf Node
    Scenario Outline: TMC is able to load Dish-VCC configuration file during initialization of CSP Master Leaf Node
        Given a TMC is using default version of dish vcc map
        When I restart the CSP Master Leaf Node and Central Node is UP   
        Then CSP Master Leaf Node should able to load dish vcc version set before restart 
        And TMC should report dish vcc config set to true
    
    Scenario Outline: TMC is able to load Dish-VCC configuration which is set while TMC is in operation after Restart
        Given a TMC is using default version of dish vcc map
        When I issue the command LoadDishCfg on TMC with Dish and VCC configuration file
        Then TMC displays the version of Dish and VCC configuration   
        When I restart the Central Node and CSP master leaf node
        Then TMC should set version of Dish Vcc used before restart 