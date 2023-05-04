Feature: TMC executes successive configure commands
    Scenario: TMC validates multiple/reconfigure functionality-different configuration
        Given the TMC is On
        And the subarray is in IDLE obsState
        When the first command Configure is issued  
        Then the subarray transitions to obsState READY
        When the next successive Configure command is issued
        Then the subarray reconfigures, transitions to obsState READY
        And tear down