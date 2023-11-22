@SP-3715
Feature: Enable and Demonstrate 5-point calibration using TMC
	#*See:*
	# * SP-3630 for corresponding SDP feature.
	# * SP-3705 for related OSO feature.
	#
	#*Who?*
	# * Control system developers.
	# * SDP real-time pipeline developers.
	# * Commissioning scientists.
	#
	#*What?*
	# * Integrated Mid software system (including TMC, Dish LMC, SDP (coordinate with SP-3630),  and OSO-scripting (coordinate with SP-3705)) capable of executing pointing offset calibration observations.
	# * A manual test of the integrated system working on a simulated five-point reference pointing observation, driven by a Jupiter notebook.
	#
	#*Why?*
	# * This functionality is required early in Mid AA0.5 commissioning.
	# * Opportunity to validate the interfaces between OSO-scripting, TMC, Dish LMC and SDP for this observing mode.

	
	@XTP-28839
	Scenario: TMC implements five point calibration scan: TMC executes Science scan after calibration successfully.
		Scenario Outline: TMC behaviour during a science scan after a five point calibration scan.
		    Given a TMC
		    And a subarray post five point calibration
		    When I invoke Configure command for a science scan
		    Then the subarray fetches calibration solutions from SDP and applies them to the Dishes
		    And is in READY obsState