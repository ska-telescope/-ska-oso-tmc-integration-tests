Feature:  Invalid unexpected commands

	Scenario: Invalid unexpected commands not allowed in the current stable obsState
		Given the TMC device/s state=On and obsState <initial_obsstate>
		When the command <unexpected_command> is invoked , throws an error
		Then the TMC device remains in state=On, and obsState <initial_obsstate>
		Examples:  
            | initial_obsstate | unexpected_command      |
            | EMPTY            | Configure               |
