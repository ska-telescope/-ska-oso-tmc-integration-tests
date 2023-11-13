@XTP-28567
Feature:  TMC executes Configure command successfully. 

    Scenario: Successful Configuration of Low Telescope Subarray in TMC
		Given a TMC
		Given a subarray in the IDLE state
		When I configure it for a scan
		Then the subarray must be in the READY state

