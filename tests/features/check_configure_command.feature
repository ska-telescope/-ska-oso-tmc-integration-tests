@XTP-28567
Feature:  TMC executes Configure command successfully. 

    Scenario: TMC validates Configure functionality
        Given the TMC is On
        And the subarray is in IDLE obsState
        When the command End is invoked 
        Then the subarray transitions to obsState IDLE