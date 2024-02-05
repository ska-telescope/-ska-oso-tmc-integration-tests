Feature: TMC handles initialization scenarios of setting and verifying Dish ID - VCC map
	@XTP-30249 @XTP-28347 @Team_HIMALAYA
	Scenario: TMC is able to load Dish-VCC configuration file during initialization of CspMasterLeafNode
		Given TMC with default version of dish vcc map
		When I restart the CspMasterLeafNode and CentralNode is running   
		Then CSP Master Leaf Node should able to load Dish-VCC version set before restart 
		And TMC should report Dish-VCC config set to true
