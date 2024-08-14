Feature: Executing an observation defined by a Scheduling Block

  Scenario Outline: Executing a Scheduling Block on a MID sub-array using standard observing scripts
    Given a telescope control system
    And EMPTY subarray 1
    When I run <script> on subarray 1 with SBD <sbd>
    Then the subarray obsState passes through RESOURCING <RESOURCING> times
    And the subarray obsState passes through CONFIGURING <CONFIGURING> times
    And the subarray obsState passes through SCANNING <SCANNING> times
    And the final obsState is <final_state>

  Examples:
    | script                         | sbd                      | RESOURCING | CONFIGURING | SCANNING  | final_state |
    | allocate_and_observe_sb.py     | mid/assign_only.json     | 2          | 0           | 0         | EMPTY       |
    | allocate_and_observe_sb.py     | mid/single_scan_sb.json  | 2          | 1           | 1         | EMPTY       |
    | allocate_and_observe_sb.py     | mid/multi_scan_sb.json   | 2          | 2           | 2         | EMPTY       |
  #  | allocate_and_observe_sb.py     | mid/5_point_example.json  | 2          | 7           | 7         | EMPTY       |
