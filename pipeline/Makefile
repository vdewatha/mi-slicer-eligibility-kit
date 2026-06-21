.PHONY: setup data data-synthetic ingest qc infer metrics export figures validate test check

ROOT := $(abspath ..)
VENV := $(ROOT)/.venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
DATA_DIR := $(ROOT)/data
PORTFOLIO_ASSETS := $(ROOT)/portfolio/assets
SCRIPTS := $(ROOT)/scripts

setup:
	python3 -m venv "$(VENV)"
	"$(PIP)" install --upgrade pip
	"$(PIP)" install -e ".[dev]"

data:
	"$(SCRIPTS)/download-sample-data.sh"

data-synthetic:
	"$(PYTHON)" -m medasset.synthetic --output-dir "$(DATA_DIR)"

ingest: setup
	"$(PYTHON)" -m medasset.cli --data-dir "$(DATA_DIR)" ingest

qc: setup
	"$(PYTHON)" -m medasset.cli --data-dir "$(DATA_DIR)" qc --output "$(PORTFOLIO_ASSETS)/qc-report.json"

infer: setup
	"$(PYTHON)" -m medasset.cli --data-dir "$(DATA_DIR)" infer

metrics: setup
	"$(PYTHON)" -m medasset.cli --data-dir "$(DATA_DIR)" metrics --output "$(PORTFOLIO_ASSETS)/segmentation-metrics.json"

export: setup
	"$(PYTHON)" -m medasset.cli --data-dir "$(DATA_DIR)" export --output-dir "$(DATA_DIR)/exports"

figures: setup
	"$(PYTHON)" -m medasset.cli --data-dir "$(DATA_DIR)" figures --output-dir "$(PORTFOLIO_ASSETS)"
	"$(ROOT)/scripts/sync-readme-images.sh"

validate: setup data-synthetic ingest qc infer metrics export figures
	"$(PYTHON)" -m medasset.cli --data-dir "$(DATA_DIR)" validate --golden "$(PORTFOLIO_ASSETS)/segmentation-metrics.json"

test: setup
	"$(PYTHON)" -m pytest tests/ -v

check:
	"$(SCRIPTS)/check-portfolio.sh"
