@XTP-28568
Feature:  TMC executes End command successfully. 
    Scenario: TMC validates End functionality
        Given the Telescope is On State
        And the subarray is in obsState READY
        When the End command is invoked 
        Then the subarray transitions to obsState IDLE
