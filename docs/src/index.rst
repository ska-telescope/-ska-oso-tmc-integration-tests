.. HOME SECTION ==================================================

.. Hidden toctree to manage the sidebar navigation.

.. toctree::
  :maxdepth: 1
  :caption: Home
  :hidden:

  CHANGELOG

.. COMMUNITY SECTION ==================================================

.. Hidden toctree to manage the sidebar navigation.

.. toctree::
  :maxdepth: 2
  :caption: Public API Documentation
  :hidden:

  api/tmcsim

=============================
ska-oso-tmc-integration-tests
=============================

Overview
========

This project holds code used to test OSO's integration with TMC. It contains:

- OSO's TMC simulator.
- Helm charts that deploy either OSO's TMC simulator or real TMC operating in simulation mode.
- BDD tests to test integration of OSO software with TMC.

Mid and Low Simulations
========================

The OSO TMC simulator provides CentralNode and Subarray device classes which simulate the corresponding TMC classes.
As these behave the same for Mid and Low, the OSO TMC simulator uses the same classes to simulate both, with the difference
being the FQDN for the devices.

The ska-oso-tmcsim helm chart deploys 2 device services: one using a default `base_uri` of 'ska-mid' which will deploy the Mid devices
(ska-mid/tm_central/central_node` `ska-mid/tm_subarray_node/1`) and one using 'ska-low' with the Low devices (ska-mid/tm_central/central_node` `ska-mid/tm_subarray_node/1`).

These devices can be enabled/disabled individually in the Helm values, and the domain name can also be configured.

Quickstart
==========
This project uses the standard SKA Make targets to control deployment of the project and execution of project tests,
e.g., ``make k8s-install-chart``, ``make k8s-test``, and ``make k8s-uninstall-chart``. The choice of deploying real or
simulated TMC is made via the ``TMC_SIMULATION_ENABLED`` variable, which can be set to ``true`` (default) or ``false``.

To deploy OSO software and OSO's TMC simulator, execute

::

  make k8s-install-chart
  # equivalent to:
  make TMC_SIMULATION_ENABLED=true k8s-install-chart

To deploy OSO software and real TMC MID components with TMC's simulations of downstream subsystems (CSP, DISH, SDP),
execute:

::

  make TMC_SIMULATION_ENABLED=false k8s-install-chart

The deployment can be halted with the standard ``make k8s-uninstall-chart`` command.
