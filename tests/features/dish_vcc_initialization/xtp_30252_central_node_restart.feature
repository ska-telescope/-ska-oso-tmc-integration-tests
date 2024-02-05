Feature: TMC handles initialization scenarios of setting and verifying Dish ID - VCC map
	@XTP-30252 @XTP-28347 @Team_HIMALAYA
	Scenario: TMC is able to load Dish-VCC configuration file during initialization of CentralNode
		Given TMC with default version of dish vcc map
		When I restart the CentralNode and CspMasterLeafNode is running   
		Then TMC should set Dish-VCC config set to True after restart