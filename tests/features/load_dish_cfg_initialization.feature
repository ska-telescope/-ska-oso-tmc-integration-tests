Feature: TMC is able to load Dish-VCC map configuration during initialization of Central Node and CSP Master Leaf Node
    Scenario Outline: TMC is able to load Dish-VCC configuration file during initialization of CSP Master Leaf Node
        Given a TMC is using default version of dish vcc map
        When I restart the CSP Master Leaf Node and Central Node is running   
        Then CSP Master Leaf Node should able to load dish vcc version set before restart 
        And TMC should report dish vcc config set to true
    
    Scenario Outline: TMC is able to load Last set Dish-VCC configuration before restart 
        Given a TMC is using default version of dish vcc map
        When I issue the command LoadDishCfg on TMC with Dish-VCC configuration file
        Then TMC displays the version of Dish and VCC configuration   
        When I restart the Central Node and CSP master leaf node
        Then TMC should set version of Dish Vcc used before restart
    
    Scenario Outline: TMC is able to load Dish-VCC configuration file during initialization of Central Node
        Given a TMC is using default version of dish vcc map
        When I restart the Central Node and CSP Master Leaf Node is running   
        Then TMC should set dish vcc config set to True after initialization

    Scenario Outline: TMC should report dish vcc config set as False when CSP Master Leaf node not available
        Given a TMC is using default version of dish vcc map
        When I make CSP Master Leaf Node unavailable and restart Central Node   
        Then TMC should set dish vcc config set to False after initialization
        And TMC should report that csp master is unavailable