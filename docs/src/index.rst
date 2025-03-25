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

This project holds code used to test OSO's TMC Simulator. It contains the source code for the
simulator as well as a Helm chart that deploys the simulator.

Mid and Low Simulations
========================

The OSO TMC simulator provides CentralNode and Subarray device classes which simulate the corresponding TMC classes.
As these behave the same for Mid and Low, the OSO TMC simulator uses the same classes to simulate both, with the difference
being the name for the devices.

The ska-oso-tmcsim helm chart deploys 2 device services: one using a default `base_uri` of 'ska_mid' which will deploy the Mid devices
(ska_mid/tm_central/central_node` `ska_mid/tm_subarray_node/1`) and one using 'ska_low' with the Low devices (ska_low/tm_central/central_node` `ska_low/tm_subarray_node/1`).

These devices can be enabled/disabled individually in the Helm values, and the domain name can also be configured.

Quickstart
==========
This project uses the standard SKA Make targets to control deployment of the project and execution of project tests,
e.g., ``make k8s-install-chart``, ``make k8s-test``, and ``make k8s-uninstall-chart`` to start the OSO TMC simulator
and execute the integration tests. Unit and component tests can be run with ``make python-test`` without installing
the Helm charts.
