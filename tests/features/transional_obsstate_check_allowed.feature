Feature:  Invalid unexpected commands - from transitional obsStates

	Scenario: Invalid unexpected commands not allowed in the current transitional obsState
		Given the TMC device/s state=On and obsState <initial_obsstate>
		When the command <unexpected_command> is invoked, it shows an error
		Then TMC Subarray remains in <initial_obsstate> and TMC accepts next command <next_command>	
		Examples:  
            | initial_obsstate | unexpected_command      | next_command |
            | RESOURCING       | AssignResources         |   Configure  |
