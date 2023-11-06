@XTP-28568
Feature:  TMC executes End commands 
    Scenario: TMC validates END functionality
        Given the Telescope is On State
        And the subarray is in obsState READY
        When the END command is invoked 
        Then the subarray transitions to obsState IDLE
