.DEFAULT_GOAL := help

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(PYTHON) -m pip

.PHONY: help setup install env run dump-data supported-yang pyang check

help: ## Show the available commands
	@echo "NetWatch RESTCONF commands:"
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z0-9_-]+:.*## / {printf "  %-16s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: install env ## Create the environment, install dependencies, and prepare .env
	@echo "Setup complete. Update .env with the current device credentials."

$(PYTHON):
	python3 -m venv $(VENV)

install: $(PYTHON) ## Install the project dependencies into .venv
	$(PIP) install netmiko==4.7.0 requests==2.34.2 python-dotenv==1.2.3 pyang==2.7.1

env: ## Create .env from .env.example when it does not exist
	@if [ -f .env ]; then \
		echo ".env already exists; leaving it unchanged."; \
	else \
		cp .env.example .env; \
		echo "Created .env from .env.example."; \
	fi

run: ## Run the network health report
	$(PYTHON) -m netwatch.main

dump-data: ## Save the selected RESTCONF response as JSON
	$(PYTHON) -m scripts.dump_data

supported-yang: ## Retrieve the device's supported YANG module names
	$(PYTHON) -m scripts.supported_yang

pyang: ## Generate tree files from the local YANG schemas
	$(PYTHON) -m scripts.run_pyang

check: ## Check Python syntax and package imports without contacting a device
	$(PYTHON) -c 'from pathlib import Path; files = list(Path("netwatch").glob("*.py")) + list(Path("scripts").glob("*.py")) + list(Path("test").glob("*.py")); [compile(path.read_text(), str(path), "exec") for path in files]; import netwatch.api, netwatch.config, netwatch.display, netwatch.utils; print("Syntax and imports: OK")'

