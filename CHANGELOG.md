Changelog
=========

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

2.0.0
*****
* Simulator deploys to ADR-9 TRLs by default. Deployment to the old pre-ADR-9 TRLs can be triggered by setting TMCSIM_USE_OLD_TRLS environment variable at deployment time.
* *BREAKING* CentralNode device uses correct Tango nomenclature, with device property now named 'domain' instead of 'base_uri'.
* *BREAKING* TMCSimTestHarness now requires a domain to be set and does not default to TMC-Mid.

1.0.0
*****
* Renamed python package to `ska_oso_tmcsim` from `ska_oso_tmc_integration_tests.tmcsim`
* Published a Helm chart `ska-oso-tmcsim` for the Mid and Low simulators
* Relaxed Python version from `^3.10,<3.13` to `^3.10`

0.4.0
*****
* Updated to Pydantic v2.10.4 and oso-scripting v10.2.0-rc5

0.3.0
*****

* Added ability to simulate Low, effectively by making the base of the FQDN configurable
* Added InjectFaultAfter and InjectDelay commands to the SubarrayNode, as described in their doc strings

0.2.1
*****

* Patch release to resolve 'publish to CAR' failure.

0.2.0
*****

* Added TMCSimTestHarness for testing using/against OSO's TMC Simulator.
* Fixed issue with initial obsstate not being transferred to state machine.

0.1.0
*****

* Initial release.
