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
	@echo "Usage: make <option>"
	@echo "Options:"
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

create-network:  ## Creates a docker network
	docker network create bases_network

build:  ## Build api
	docker-compose build

migrate:  ## Migrate database
	docker-compose run --rm base_a flask db upgrade
	docker-compose run --rm base_a flask db migrate

seeder:  ## Seed database
	docker-compose run --rm base_a flask seed run

bash:  ## Run api bin/bash
	docker-compose run --rm runner

test: ## Run api tests
	@docker exec -it base_a_postgres psql -q -Atx ${DATABASE_URL} -c "DROP DATABASE IF EXISTS ${DATABASE}_tests"
	@docker exec -it base_a_postgres psql -q -Atx ${DATABASE_URL} -c "CREATE DATABASE ${DATABASE}_tests"

	docker-compose run --rm runner pytest --cov-report=term-missing --cov-report=html --cov=.

code-convention:  ## Run code convention
	@flake8 main.py app tests seeds
	@echo == Code convention is ok

run:  ## Run api
	docker-compose up base_a

install: create-network build migrate seeder test code-convention  ## Install api
