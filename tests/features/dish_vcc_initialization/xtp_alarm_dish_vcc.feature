Feature: TMC handles initialization scenarios of setting and verifying Dish ID - VCC map

	
	@XTP-30260 @XTP-28347 @Team_HIMALAYA
	Scenario: TMC Validates and Reports K-Value not set in Dish Leaf Nodes
		Given a TMC with already loaded Dish-VCC map version
		When the Dish Leaf Node is restarted
		And the Dish Leaf Node finds k-value not set on Dish Leaf Node
		Then the Alarm is raised for kValue not set
		And the Central Node reports the same and prohibits any further command execution