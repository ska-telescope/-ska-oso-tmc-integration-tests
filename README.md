# ska-oso-tmcsim

## Description

This project holds code used to test OSO's TMC Simulator. It contains the source code for the 
simulator as well as a Helm chart that deploys the simulator.

## Installation



### Update .make submodule

`.make` submodule contains the common SKA Makefiles managed by the System Team. It is good to keep the submodule as 
up-to-date as possible. To update the `.make` submodule to the latest version, run

```
git submodule update --init --remote .make
```

*Note: This is usually done with `make make` command but this should not be used in a project where other submodules 
are present and those submodules are not updated in-sync.

# Deployment
To deploy TMCSim to ADR-9 TRLs, run
```
make k8s-install-chart
```
To deploy TMCSim to the previous non-ADR-9 TRLs, run
```
TMCSIM_USE_OLD_TRLS=1 make k8s-install-chart
```

# Support

Issues with this project should be raised on the #team-oso Slack channel and reported via the SKA Jira system.

## Roadmap

- Improve simulation of long-running commands

## Contributing

Contributions to this project are welcome. All contributions must meet the SKA standards, which are documented at the
[SKA Developer Portal](https://developer.skao.int/en/latest/getting-started/contrib-guidelines.html).

To run SKA checks manually, run `make python-format`, `make python-lint`, and `make python-test`. We recommend doing
running these steps locally before each commit.

This project includes a [pre-commit](https://pre-commit.com/) configuration file. It is recommended to install
pre-commit to ensure that your commits always meet formatting requirements.

## License

This project is subject to the BSD 3-Clause license.
