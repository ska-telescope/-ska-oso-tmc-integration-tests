# ska-oso-tmc-integration-tests

## Description

This project holds code used to test OSO's integration with TMC. It contains:

- OSO's TMC simulator.
- Helm charts that deploy either OSO's TMC simulator or real TMC operating in simulation mode.
- BDD tests to test integration of OSO software with TMC.

> :warning: Currently, this project only targets simulation and testing for SKA MID

## Installation

No installation is required unless you want to contribute to this project. If you want to contribute, 
project requirements can be installed with `poetry install --with=dev --sync`.

## Usage

To deploy the default system, use `make k8s-install-chart`. The deployment can be customised with the following
variables:

| Variable               | Default value | Description                                                                                                                                                                                                                   |
|------------------------|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| TMC_SIMULATION_ENABLED | true          | Deploys OSO's TMC simulator (true) or TMC with simulation of other subsystems (false)                                                                                                                                         |
| TMCSIM_TAG             |               | Sets the tag to use for the TMC simulator image. This can be used to override the value in the chart, e.g, '0.0.1-dirty'.                                                                                                     |
| OET_INGRESS            | false         | Controls whether OET network ingress is enabled (true) or disabled (false). Ingress exposes an API for remote execution of Python scripts, so for security is disabled by default.                                            |
| LOCAL_ODA              | false         | Controls whether the ODA saves entities inside the ODA pod (false) or inside an `oda` directory shared with the host machine. File sharing between host machine and Minikube *must* be set up for this to function correctly. | 
| DEVENV                 | false         | Shortcut to set `OET_INGRESS` and `LOCAL_ODA` to true                                                                                                                                                                         | 

## Update submodules
When updating the version of `ska-oso-scripting` Python dependency or the chart version of `ska-tmc-mid` chart dependency, 
the corresponding submodule should be updated as well. For `ska-oso-scripting` the submodule is in `submodules/ska-oso-scripting` 
and for `ska-tmc-mid` it is in `submodules/ska-tmc-mid-integration`. To update the submodule to specific version run:

```
cd submodules/<project_name>
git checkout tags/<new_version>
cd ../..
```

Make sure to commit the changes after the update. To check that the submodules are pointing to the expected versions run

```
git submodule status
```

# Support

Issues with this project should be raised on the #team-oso Slack channel and reported via the SKA Jira system.

## Roadmap

- Improve simulation of long-running commands
- Expand OSO's TMC simulator to include simulation of TMC LOW.

## Contributing

Contributions to this project are welcome. All contributions must meet the SKA standards, which are documented at the
[SKA Developer Portal](https://developer.skao.int/en/latest/getting-started/contrib-guidelines.html).

To run SKA checks manually, run `make python-format`, `make python-lint`, and `make python-test`. We recommend doing
running these steps locally before each commit.

This project includes a [pre-commit](https://pre-commit.com/) configuration file. It is recommended to install
pre-commit to ensure that your commits always meet formatting requirements.

## License

This project is subject to the BSD 3-Clause license.
