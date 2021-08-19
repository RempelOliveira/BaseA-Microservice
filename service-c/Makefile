-include .env
export

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("	%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@echo "Usage: make <command>"
	@echo "Options:"
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

build:  ## Build api
	docker-compose build

seeder:  ## Seed database
	docker-compose run --rm base_c flask seed run --no-commit

bash:  ## Run api bin/bash
	docker-compose run --rm runner

test:  ## Run api tests
	docker-compose run --rm runner pytest --cov-report=term-missing --cov-report=html --cov=.

code-convention:  ## Run code convention
	@flake8 main.py app tests seeds
	@echo == Code convention is ok

run:  ## Run api
	docker-compose up base_c

install: build seeder test code-convention  ## Install api
