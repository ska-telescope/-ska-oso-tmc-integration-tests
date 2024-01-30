Feature: Default

	#This BDD test performs TMC-CSP pairwise testing to verify Abort command flow.
	@XTP-29838 @XTP-29583 @Team_SAHYADRI
	Scenario: Abort configuring CSP using TMC
		Given the telescope is in ON state
		And the TMC subarray <subarray_id> and CSP subarray <subarray_id> is busy in configuring
		When I issued the Abort command to the TMC subarray <subarray_id>
		Then the CSP subarray <subarray_id> transitions to ObsState ABORTED
		And the TMC subarray <subarray_id> transitions to ObsState ABORTED
		Examples:
		    | subarray_id |
		    | 1           |