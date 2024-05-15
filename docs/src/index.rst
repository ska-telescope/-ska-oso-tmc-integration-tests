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

Currently, this project only targets simulation and testing for SKA MID.

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
