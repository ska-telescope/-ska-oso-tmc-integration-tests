@XTP-28568
Feature:  TMC executes End commands 
    Scenario: TMC validates configure functionality
        Given the TMC is On
        And the subarray is in IDLE obsState
        When the command Configure is invoked with correct input_json
        Then the subarray transitions to obsState READY
