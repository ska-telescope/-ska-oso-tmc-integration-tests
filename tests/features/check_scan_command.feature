@XTP-28568
Feature:  TMC executes Scan command successfully. 

    Scenario: Successful Execution of Scan Command on Low Telescope Subarray in TMC
    Given a TMC
    Given a subarray in READY state
    When I command it to scan for a given period
    Then the subarray must be in the SCANNING state until finished
    And test goes for the tear down
