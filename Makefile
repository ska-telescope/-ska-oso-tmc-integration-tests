CAR_OCI_REGISTRY_HOST := artefact.skao.int
CI_PROJECT_PATH_SLUG ?= ska-oso-tmc-integration-tests
CI_ENVIRONMENT_SLUG ?= ska-oso-tmc-integration-tests

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
PYTHON_SWITCHES_FOR_BLACK = --exclude="tests/integration/tests/tmcmid/conftest.py"

PYTHON_SWITCHES_FOR_ISORT =

# Restore Black's preferred line length which otherwise would be overridden by
# System Team makefiles' 79 character default
PYTHON_LINE_LENGTH = 88

# Set python-test make target to only run unit tests, as tests in the integration
# folder require Tango.
PYTHON_TEST_FILE = tests/unit

#- Kubernetes test configuration ------------------------------------------------------

# override k8s-test so that:
# - pytest --forked is run, working around Tango segfault issue with standard pytest
# - only integration tests run and unit tests are ignored
# - adds 'rP' to print captured output for successful tests
K8S_TEST_TEST_COMMAND = $(PYTHON_VARS_BEFORE_PYTEST) $(PYTHON_RUNNER) \
                        ODA_URL=$(ODA_URL) \
                        pytest --forked -rP \
                        $(PYTHON_VARS_AFTER_PYTEST) ./tests/integration \
                         | tee pytest.stdout ## k8s-test test command to run in container

#- Kubernetes configuration -----------------------------------------------------------


# KUBE_NAMESPACE defines the Kubernetes Namespace that will be deployed to
# using Helm.  If this does not already exist it will be created
ifneq ($(CI_JOB_ID),)
KUBE_NAMESPACE ?= ci-$(CI_PROJECT_NAME)-$(CI_COMMIT_SHORT_SHA)
OCI_REGISTRY ?= registry.gitlab.com/ska-telescope/oso/ska-oso-tmc-integration-tests
else
OCI_REGISTRY ?= artefact.skao.int
endif

MINIKUBE ?= false ## Is this deployment running in Minikube? true/false
MINIKUBE_IP = $(shell minikube ip)
HOSTNAME = $(shell hostname)

DATABASEDS = tango-databaseds  ## TANGO_HOST connection to the Tango DS
CLUSTER_DOMAIN ?= cluster.local
TANGO_PORT ?= 10000
TANGO_HOST ?= $(strip $(DATABASEDS)):$(strip $(TANGO_PORT))

# Enable Taranta deployment. true/false
TARANTA_ENABLED ?= false

ODA_URL ?= http://ska-db-oda-rest-$(HELM_RELEASE):5000/$(KUBE_NAMESPACE)/oda/api/v3

K8S_CHART_PARAMS = --set global.minikube=$(MINIKUBE) \
	--set global.tango_host=$(TANGO_HOST) \
	--set global.exposeAllDS=false \
	--set global.cluster_domain=$(CLUSTER_DOMAIN) \
	--set global.operator=true \
	--set ska-taranta.enabled=$(TARANTA_ENABLED)\
    --set ska-db-oda.pgadmin4.enabled=false\
	--set ska-db-oda.rest.backend.type=filesystem\
    --set ska-db-oda.postgresql.enabled=false\
    --set ska-oso-oet.rest.oda.backend.type=rest\
    --set ska-oso-oet.rest.oda.url=$(ODA_URL)\
	--set ska-oso-tmcsim.image.registry=$(OCI_REGISTRY)

# tag to use when deploying TMC simulator
TMCSIM_TAG ?= $(VERSION)

# Simulate TMC: true / false
TMC_SIMULATION_ENABLED ?= true
ifeq ($(TMC_SIMULATION_ENABLED),false)
K8S_CHART_PARAMS += 	--set ska-tmc-mid.enabled=true\
	--set ska-oso-tmcsim.enabled=false\
	--set ska-tango-alarmhandler.enable=true\
	--set tmc-mid.deviceServers.mocks.dish=true\
	--set tmc-mid.subarray_count=1
else
K8S_CHART_PARAMS += 	--set ska-tmc-mid.enabled=false\
	--set ska-tango-alarmhandler.enable=false\
	--set ska-oso-tmcsim.enabled=true\
    --set ska-oso-tmcsim.image.tag=$(TMCSIM_TAG)
endif

# write ODA entities to local filesystem. Filesharing with Minikube MUST be set up!
LOCAL_ODA ?= false
ifeq ($(LOCAL_ODA),true)
K8S_CHART_PARAMS +=	--set ska-db-oda.rest.backend.filesystem.use_pv=true\
    --set ska-db-oda.rest.backend.filesystem.pv_hostpath=$(PWD)/oda
endif

# Expose OET API and Swagger UI
OET_INGRESS ?= false
ifeq ($(OET_INGRESS),true)
K8S_CHART_PARAMS +=	--set ska-oso-oet.rest.ingress.enabled=true
endif

# Developer environment setup. Shortcut for activating options useful for developers,
# e.g., open ingress and ODA with local filesystem backing.
DEVENV ?= false
ifeq ($(DEVENV),true)
MINIKUBE = true
LOCAL_ODA = true
OET_INGRESS = true
endif

#- Make target customisation ----------------------------------------------------------

k8s-pre-install-chart:
ifeq ($(LOCAL_ODA),true)
	export ODA_DIR=$(PWD)/oda && \
	echo "Creating ODA backing directory $$ODA_DIR..." && \
	mkdir -p $$ODA_DIR
endif

k8s-post-install-chart:
ifneq ($(MINIKUBE_IP),)
ifeq ($(TARANTA_ENABLED), true)
	@echo "    * Taranta: http://$(MINIKUBE_IP)/$(KUBE_NAMESPACE)/taranta/"
endif
ifeq ($(OET_INGRESS),true)
	@echo "    * OET Swagger UI: http://$(MINIKUBE_IP)/$(KUBE_NAMESPACE)/oet/api/v6/ui"
	@echo "    * OET REST API: http://$(MINIKUBE_IP)/$(KUBE_NAMESPACE)/oet/api/v6"
endif
	@echo "    * ODA Swagger UI: http://$(MINIKUBE_IP)/$(KUBE_NAMESPACE)/oda/api/v3/ui"
	@echo "    * ODA REST API: http://$(MINIKUBE_IP)/$(KUBE_NAMESPACE)/oda/api/v3"
endif
ifeq ($(DEVENV), true)
	@echo
	@echo "To connect to the Tango database from your host, run"
	@echo
	@echo "    kubectl -n $(KUBE_NAMESPACE) port-forward services/tango-databaseds $(TANGO_PORT)"
	@echo "    export TANGO_HOST=$(TANGO_HOST)"
endif


devpod: DEVENV = true
devpod: K8S_CHART_PARAMS += --set ska-oso-devpod.enabled=true\
	--set ska-oso-devpod.image.tag=$(TMCSIM_TAG)\
	--set ska-oso-devpod.env.oda_url=$(ODA_URL)\
	--set ska-oso-devpod.hostPath=$(PWD)
devpod: k8s-install-chart
	@echo "Waiting for devpod to become available..."
	@kubectl -n $(KUBE_NAMESPACE) wait --for=condition=ready pod devpod
	@echo "Now launching a bash terminal inside devpod..."
	@kubectl -n $(KUBE_NAMESPACE) exec --stdin --tty devpod -- /bin/bash
