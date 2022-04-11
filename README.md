# TMC-integration-test

This section contains the testing scripts and configuration data for performing end to end tests on the TMC.

## Concepts 

The tests aims to replicate a user operating on the system to achieve a set of user requirements. To help with automation the interface is via a text based interactive OET console. Thus the entrypoint into the system is on the OET. Future tests should also explore the greater use of GUI's (e.g. webjive) as entry points.

To observe the system requires looking at the internal state of the system. This is currently implemented using the TANGO framework but in future may include accessing the kubernetes framework and other SDP related communication frameworks.

## Architecture

To ensure the test scripts are executing via the OET they have to be invoked on an exact replica of the OET execution environment. Thus the container (and therefore pod) used in performing the test must be loaded with the exact same image (or package) that will be used in deploying the TMC during production. For testing the TMC in the CI pipeline this is acheived by ensuring the test runner is loaded with the same container image as used for the oet. During development the user can make use of an interactive pod that gets deployed with a ska-tmc-integration repository as its volume using the same image as for the oet container.

Note that during interactive development the testing deployment consists of two parts:

1. The git storage (Persistance Volume CLaim and Persistance Volume)
2. The test pod (mounting on the storage)

The git storage allows the ska-tmc-integration repository to be mounted as a volume onto the container. This allows the tester to interactively work on the testing scripts whilst executing them on an container instance.

## Getting Started

### Running tests automatically

To run a test autimatically the test runner pod is used as deployed by the ci pipeline. This forms part of the general testing that gets run during the testing stage and gets invoked by:

```shell
make K8s_test:
```
Note that the testing configuration is set up so that it will ignore tests ending with "_dev". This allows one to isolate tests that are committed to master but not yet released for testing the pipeline.

Before commiting your code to master make sure the the tests execute during the test pipeline by running above command.