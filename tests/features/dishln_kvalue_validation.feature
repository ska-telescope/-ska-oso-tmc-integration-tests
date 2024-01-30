Scenario Outline: TMC Validates and Reports K-Value set in Dish Leaf Nodes
    Given a TMC is using the default version of the dish vcc map
    When the Dish Leaf Node is restarted
    And the Dish Leaf Node finds k-value set on Dish Leaf Node and Dish Manager are identical
    Then Dish Leaf Node reports it to the Central Node
    And the Central Node continues with current operation as their are no discrepancies

Scenario Outline: TMC Validates and Reports K-Value discrepancy in Dish Leaf Nodes
    Given a TMC is using the default version of the dish vcc map
    When the Dish Leaf Node is restarted
    And the Dish Leaf Node finds the k-value set on either of the Dish Leaf Node and Dish Manager are not identical
    Then Dish Leaf Node reports this discrepancy to the Central Node
    And the Central Node reports the same and prohibits any further command execution    

Scenario Outline: TMC Validates and Reports K-Value not set in Dish Leaf Nodes
    Given a TMC is using the default version of the dish vcc map
    When the Dish Leaf Node is restarted
    And the Dish Leaf Node finds k-value not set on either of Dish Leaf Node or Dish Manager
    Then Dish Leaf Node reports it to the Central Node
    And the Central Node reports the same and prohibits any further command execution