Feature: Successfully execute a scan after a failed configure
	#The scenario is provided to convey the intention, it should refined: 
	#The test should be repeated for at least two cases:
	#a) the first Configure command passes an invalid (malformed) JSON script
	#b) the first Configure command  passes a JSON script that uses resources which are not assigned to the subarray. 
	#Error reporting for cases a) and b) may be different 
	@XTP-20321 @XTP-28347 @End_to_end @configuration
	Scenario: "Successful scan after failed configure, using same resources",
		Given a subarray <subarray_id> with resources <resources_list> in obsState IDLE
		When I issue the command Configure passing an invalid JSON script to the subarray <subarray_id>
		Then the subarray <subarray_id> returns an error message
		And the subarray <subarray_id> remains in obsState IDLE 
		When I issue the command Configure passing a correct JSON script  
		Then the subarray transitions to obsState READY
		When I issue the command Scan  
		Then the subarray transitions to obsState SCANNING
		When I issue the command EndScan  
		Then the subarray transitions to obsState READY
		And the data is recorced as expected

        Examples:
            | subarray_id  | resources_list |
            | 1            | "SKA001"       |