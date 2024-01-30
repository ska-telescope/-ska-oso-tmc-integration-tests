Feature: Default

	#This BDD test performs TMC-CSP pairwise testing to verify Abort command flow.
	@XTP-29840 @XTP-29583 @Team_SAHYADRI
	Scenario: Abort assigning CSP using TMC
		Given the telescope is in ON state
		And TMC subarray <subarray_id> and CSP subarray <subarray_id> busy assigning
		When I issued the Abort command to the TMC subarray <subarray_id>
		Then the CSP subarray <subarray_id> transitions to ObsState ABORTED
		And the TMC subarray <subarray_id> transitions to ObsState ABORTED
		Examples:
		    | subarray_id |
		    | 1           |