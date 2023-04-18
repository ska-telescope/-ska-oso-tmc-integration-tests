Feature:  Invalid unexpected commands - from transitional obsStates

	Scenario: Invalid unexpected commands not allowed in the current transitional obsState
		Given the TMC device/s state=On and obsState <initial_obsstate>
		When the command <unexpected_command> shows an error
		Then the TMC device remains in state=On, and obsState <initial_obsstate>
		
		Examples:  
            | initial_obsstate | unexpected_command      |
            | RESOURCING       | AssignResources         |
