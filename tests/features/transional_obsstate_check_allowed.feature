Feature:  Invalid unexpected commands - from transitional obsStates

	Scenario: Invalid unexpected commands not allowed in the current transitional obsState
		Given the TMC device/s state=On and obsState <initial_obsstate>
		When the command <unexpected_command> is invoked
		Then the command <unexpected_command> shows an error
		And the TMC device remains in state=On, and obsState <initial_obsstate>
		And TMC accepts correct/expected command <expected_command> and performs the operation
		
		Examples:  
            | initial_obsstate | unexpected_command      |
            | RESOURCING       | AssignResources         |
