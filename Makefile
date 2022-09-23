PACKAGE_NAME ?= github.com/tigera/anomaly_detection_jobs
GO_BUILD_VER ?= v0.72

ORGANIZATION := tigera
SEMAPHORE_PROJECT_ID ?= $(SEMAPHORE_ANOMALY_DETECTION_JOBS_PROJECT_ID)

ADJ_IMAGE             ?=tigera/anomaly_detection_jobs
BUILD_IMAGES          ?=$(ADJ_IMAGE)
DEV_REGISTRIES        ?=gcr.io/unique-caldron-775/cnx
RELEASE_REGISTRIES    ?=quay.io
RELEASE_BRANCH_PREFIX ?=release-calient
DEV_TAG_SUFFIX        ?=calient-0.dev
ARCHES                ?=amd64
###############################################################################
# Download and include Makefile.common
#   Additions to EXTRA_DOCKER_ARGS need to happen before the include since
#   that variable is evaluated when we declare DOCKER_RUN and siblings.
###############################################################################
MAKE_BRANCH ?= $(GO_BUILD_VER)
MAKE_REPO ?= https://raw.githubusercontent.com/projectcalico/go-build/$(MAKE_BRANCH)

Makefile.common: Makefile.common.$(MAKE_BRANCH)
	cp "$<" "$@"
Makefile.common.$(MAKE_BRANCH):
	# Clean up any files downloaded from other branches so they don't accumulate.
	rm -f Makefile.common.*
	curl --fail $(MAKE_REPO)/Makefile.common -o "$@"

include Makefile.common

AD_JOB_INTEG_IMAGE ?= tigera/anomaly_detection_jobs_integ

ES_CONTAINER_NAME := "ad-job-integ-elasticsearch"
ELASTIC_USER := elastic
BOOTSTRAP_PASSWORD := $(shell cat /dev/urandom | LC_CTYPE=C tr -dc A-Za-z0-9 | head -c16)
ELASTIC_PASSWORD := $(BOOTSTRAP_PASSWORD)
# retrieves net ip of host as fv docker contianer needs to communicate with the elastichsearch container
ELASTIC_HOST := $(shell hostname -I | cut -f1 -d' ')
ELASTIC_PORT := 9200
# installation requirements
REQUIRED_PYTHON_VERSION := 3.8
PYTHON_VERSION := $(shell python3 -c "import sys;t='{v[0]}.{v[1]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)")
POETRY_OFFICIAL := https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py
REQUIRED_POETRY_VERSION := 1.1.10
POETRY_HOME := ${HOME}/.poetry
POETRY_VIRTUALENVS_PATH := ${HOME}/.cache/pypoetry/virtualenvs
# polyaxon
POLYAXON_CLI_VERSION := 1.20.0
POLYAXON_HOST := https://polyaxon.dev.calicocloud.io
POLYAXON_TOKEN ?= ""
POLYAXON_OWNER := tigera
POLYAXON_PROJECT := PRODUCTION
POLYAXON_DOWNLOAD_PATH := /tmp/plx/download
POLYAXON_MODELS_PATH := ./models/prod/dynamic
POLYAXON_OUTPUTS_PATH := ./outputs
# ci related variables
SKIP_COVERAGE ?= true
COVERAGE_FILENAME := coverage_report

# Python commands need to check that correct Python version is installed
python_cmds = lint ut
$(python_cmds) : pyversion-check

# These commands always need to be executed
.PHONY: pyversion-check install-poetry install\
			 update-dependencies upgrade-poetry\
			 test ut fv ci cd \
			 download-and-restructure-prod-models clean-model-download \

clean-model-download:
	rm -rf ${POLYAXON_DOWNLOAD_PATH}

download-and-restructure-prod-models: clean-model-download
	python -m pip install polyaxon==${POLYAXON_CLI_VERSION}
	polyaxon config set --host ${POLYAXON_HOST}
	polyaxon login -t ${POLYAXON_TOKEN}
	polyaxon init --project="${POLYAXON_OWNER}/${POLYAXON_PROJECT}" -y
	@echo "List of the current registered models to the production model registry"
	polyaxon models ls
	mkdir -p ${POLYAXON_DOWNLOAD_PATH}
	polyaxon models pull --query "stage: production" --path ${POLYAXON_DOWNLOAD_PATH}
	python3 scripts/restructure_prod_models.py \
		--download_path=${POLYAXON_DOWNLOAD_PATH} \
		--prod_models_path=${POLYAXON_MODELS_PATH} \
		--polyaxon_outputs_path=${POLYAXON_OUTPUTS_PATH}

##########################################################################################
# Continuous Integration
##########################################################################################
ci-build: install
ci-test: ut
ci-analysis: lint
ci-run: ci-analysis ci-test
ci: | ci-build ci-run

##########################################################################################
# Continuous Deployment
##########################################################################################
cd: image cd-common
image: download-and-restructure-prod-models
	docker build -t $(ADJ_IMAGE):latest-$(ARCH) -f Dockerfile .

ifeq ($(ARCH),amd64)
	docker tag $(ADJ_IMAGE):latest-$(ARCH) $(ADJ_IMAGE):latest
endif

dev-image: download-and-restructure-prod-models
	docker build --target development -t $(ADJ_IMAGE)-dev:latest -f Dockerfile .

##########################################################################################
# Install
##########################################################################################
pyversion-check:
ifneq ("${REQUIRED_PYTHON_VERSION}", "${PYTHON_VERSION}")
	@echo "Current python version ${PYTHON_VERSION} must match the required version ${REQUIRED_PYTHON_VERSION}"
	exit 1
endif

install-poetry: pyversion-check
ifeq (, $(shell which poetry))
	curl -sSL ${POETRY_OFFICIAL} | POETRY_HOME=${POETRY_HOME} POETRY_VERSION=${REQUIRED_POETRY_VERSION} python3 -
	$(shell source ${POETRY_HOME}/env)
endif

install: pyversion-check install-poetry
ifeq (, $(shell which poetry))
	@echo "poetry is not installed, run 'make install-poetry'"
else
	poetry config virtualenvs.path ${POETRY_VIRTUALENVS_PATH}
	poetry env use python3
	poetry check
	@echo "Using virtualenvs located at ${POETRY_VIRTUALENVS_PATH}/$(shell poetry env list)"
	poetry install --no-interaction --no-ansi
	poetry run pre-commit install
endif

update-dependencies: install
	poetry update
	rm poetry.lock
	poetry lock

upgrade-poetry:
	poetry self update ${REQUIRED_POETRY_VERSION}

uninstall-poetry:
	curl -sSL ${POETRY_OFFICIAL} | python3 - --uninstall -y

##########################################################################################
# Lint
##########################################################################################
lint:
	poetry run isort --check adj tests
	poetry run black --check adj tests
	poetry run pycodestyle adj tests --exclude ".banzai" --exclude ".bz"
	poetry run mypy adj tests

format:
	poetry run isort adj tests
	poetry run black adj tests

##########################################################################################
# TESTS
##########################################################################################
test: image

# By default, tests will be tiny-bit verbose and starting from last failed (if any).
# Additionally, tests are summarised and ordered based on their duration.
PYTEST_ARGS=--log-level "DEBUG" -v --durations 0 --maxfail 1
ifneq ("$(SKIP_COVERAGE)", "true")
	PYTEST_ARGS+= --cov=adj --junitxml $(COVERAGE_FILENAME).xml --cov-report term:skip-covered
endif

ut:
	POLYAXON_NO_OP=true USE_PRETRAIN=false poetry run pytest ${PYTEST_ARGS} tests
ifneq ("$(SKIP_COVERAGE)", "true")
	mv $(COVERAGE_FILENAME).xml $(COVERAGE_FILENAME)_ut.xml
endif

fv:
	poetry run pytest ${PYTEST_ARGS} tests/fv
ifneq ("$(SKIP_COVERAGE)", "true")
	mv $(COVERAGE_FILENAME).xml $(COVERAGE_FILENAME)_fv.xml
endif

ut-fv:
	poetry run pytest ${PYTEST_ARGS} tests/

unify-junit-reports:
	poetry run python ./scripts/merge_junitxml_reports.py $(COVERAGE_FILENAME)_* > $(COVERAGE_FILENAME).xml

create-code-coverage:
	poetry run coverage html --directory code_coverage
