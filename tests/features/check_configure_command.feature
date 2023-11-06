@XTP-28567
Feature:  TMC executes Configure commands 
    Scenario: TMC validates End functionality
        Given the TMC is On
        And the subarray is in READY obsState
        When the command End is invoked 
        Then the subarray transitions to obsState IDLE