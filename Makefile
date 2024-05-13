CAR_OCI_REGISTRY_HOST := artefact.skao.int
CI_PROJECT_PATH_SLUG ?= ska-oso-tmc-integration-tests
CI_ENVIRONMENT_SLUG ?= ska-oso-tmc-integration-tests

-include .make/base.mk
-include .make/python.mk
-include .make/oci.mk
-include PrivateRules.mak

# unset defaults so settings in pyproject.toml take effect
PYTHON_SWITCHES_FOR_BLACK =
PYTHON_SWITCHES_FOR_ISORT =

# Restore Black's preferred line length which otherwise would be overridden by
# System Team makefiles' 79 character default
PYTHON_LINE_LENGTH = 88
