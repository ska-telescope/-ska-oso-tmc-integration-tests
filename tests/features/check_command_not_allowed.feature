Feature:  Invalid unexpected commands

	Scenario: Invalid unexpected commands not allowed in the current stable obsState
		Given the TMC device/s state=On and obsState <initial_obsstate>
		When the command <unexpected_command> is invoked , throws an error
		Then the TMC device remains in state=On, and obsState <initial_obsstate>
		Then TMC accepts correct/expected command <expected_command> and performs the operation
		Examples:  
            | initial_obsstate | unexpected_command      | expected_command |
            | EMPTY            | Configure               | AssignResources  |
            | EMPTY            | Scan                    | AssignResources  |
			| EMPTY			   | End					 | AssignResources	|

	Scenario: Invalid unexpected commands not allowed in the current stable obsState - Idle
		Given the TMC device/s state=On and obsState <initial_obsstate>
		When the command <unexpected_command> is invoked , throws an error
		Then the TMC device remains in state=On, and obsState <initial_obsstate>
		Then TMC accepts correct/expected command <expected_command> and performs the operation
		Examples:  
            | initial_obsstate | unexpected_command      | expected_command  |
            | IDLE            | Scan                     | ReleaseResources  |
            | IDLE            | End                      | ReleaseResources  |