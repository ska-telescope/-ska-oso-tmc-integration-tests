Feature: Allocate resources to a subarray

  Scenario Outline: Allocation to a MID sub-array using standard observing scripts
    Given a telescope control system
    And EMPTY subarray 1
    When I run <script> on subarray 1 with SBD <sbd>
    Then the subarray obsState passes through RESOURCING <RESOURCING> times
    And the subarray obsState passes through CONFIGURING 0 times
    And the subarray obsState passes through SCANNING 0 times
    And the final obsState is <final_state>

  Examples:
    | script                         | sbd                   | RESOURCING | final_state |
    | allocate_and_observe_mid_sb.py | mid/assign_only.json  | 2          | EMPTY       |
#    | allocate_from_file_mid_sb.py   | mid/assign_only.json  | 1          | IDLE        |
