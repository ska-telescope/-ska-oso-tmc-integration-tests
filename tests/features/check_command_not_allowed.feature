Feature:  Invalid unexpected commands

	Scenario: Invalid unexpected commands not allowed in the current stable obsState
		Given the TMC device/s state=On and obsState <initial_obsstate>
		When the command <unexpected_command> shows an error
		Then the TMC device remains in state=On, and obsState <initial_obsstate>
		And TMC accepts correct/expected command <expected_command> and performs the operation
		Examples:  
            | initial_obsstate | unexpected_command      |     expected_command    |
            | EMPTY            | Configure               |      AssignResources    |
