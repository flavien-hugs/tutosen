VENV := env
BIN := $(VENV)/bin
SHELL := /bin/bash
MANAGE := python manage.py

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: venv
venv: ## Make a new virtual environment
	pip3 install pipenv
	pipenv shell

.PHONY: install
install: venv ## Install or update dependencies
	pipenv install

freeze: ## Pin current dependencies
	pipenv run pip freeze > requirements.txt

migrate: ## Make and run migrations
	$(MANAGE) makemigrations
	$(MANAGE) migrate

createsuperuser: ## Run the Django server
	$(MANAGE) createsuperuser --email="ssh.unsta@pm.me"

changepassword: ## Change password superuser
	$(MANAGE) changepassword ssh.unsta@pm.me

collectstatic: ## Run collectstatic
	$(MANAGE) collectstatic --noinput
