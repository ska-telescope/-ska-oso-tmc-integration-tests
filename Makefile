CAR_OCI_REGISTRY_HOST := artefact.skao.int
CI_PROJECT_PATH_SLUG ?= ska-oso-tmcsim
CI_ENVIRONMENT_SLUG ?= ska-oso-tmcsim

K8S_CHART = ska-oso-tmcsim

-include .make/base.mk
-include .make/helm.mk
-include .make/k8s.mk
-include .make/oci.mk
-include .make/python.mk
-include PrivateRules.mak

#- doc configuration ------------------------------------------------------------------

# Fail the docs build if there is a warning (eg if the autoimports are not configured)
# https://www.sphinx-doc.org/en/master/man/sphinx-build.html#cmdoption-sphinx-build-W
DOCS_SPHINXOPTS=-W --keep-going


#- Python configuration ---------------------------------------------------------------


# unset defaults so settings in pyproject.toml take effect
PYTHON_SWITCHES_FOR_BLACK =

PYTHON_SWITCHES_FOR_ISORT =

# Restore Black's preferred line length which otherwise would be overridden by
# System Team makefiles' 79 character default
PYTHON_LINE_LENGTH = 88

## Configure unit and component test run (make python-test target) so that:
## - pytest --forked is run, working around Tango segfault issue with standard pytest
## - adds 'rP' to print captured output for successful tests
PYTHON_TEST_FILE = tests/unit tests/component
PYTHON_VARS_AFTER_PYTEST += --forked -rP

# tango_host is defined in the values.yaml but we need to redefine it here so that we
# can inject the TANGO_HOST environment variable to the k8s-test pod. This should match
# what is defined in the values.yaml as global.tango_host
DATABASEDS = tango-databaseds
TANGO_PORT ?= 10000
TANGO_HOST ?= $(strip $(DATABASEDS)):$(strip $(TANGO_PORT))

K8S_TEST_TEST_COMMAND = $(PYTHON_VARS_BEFORE_PYTEST) \
						$(PYTHON_RUNNER) \
                        pytest \
                        $(PYTHON_VARS_AFTER_PYTEST) ./tests/integration \
                         | tee pytest.stdout ## k8s-test test command to run in container
K8S_TEST_RUNNER_ADD_ARGS = --env=TANGO_HOST=$(TANGO_HOST)

#- Kubernetes configuration -----------------------------------------------------------


# When running jobs on the pipeline, pull the GitLab version of the image rather than one from CAR
ifneq ($(CI_JOB_ID),)
K8S_CHART_PARAMS += --set image.registry=$(CI_REGISTRY)/ska-telescope/oso/ska-oso-tmcsim #--set image.tag=$(VERSION)-dev.c$(CI_COMMIT_SHORT_SHA) \
#	--set image.registry=$(CI_REGISTRY)/ska-telescope/oso/ska-oso-tmcsim
else
OCI_REGISTRY ?= artefact.skao.int
K8S_CHART_PARAMS += --set global.cluster_domain="cluster.local"
endif


MINIKUBE ?= false ## Is this deployment running in Minikube? true/false
MINIKUBE_IP = $(shell minikube ip)
HOSTNAME = $(shell hostname)

DATABASEDS = tango-databaseds  ## TANGO_HOST connection to the Tango DS
CLUSTER_DOMAIN ?= cluster.local
TANGO_PORT ?= 10000
TANGO_HOST ?= $(strip $(DATABASEDS)):$(strip $(TANGO_PORT))

K8S_CHART_PARAMS += --set global.minikube=$(MINIKUBE)
#	--set global.tango_host=$(TANGO_HOST) \
#	--set global.exposeAllDS=false \
#	--set global.cluster_domain=$(CLUSTER_DOMAIN) \
#	--set global.operator=true