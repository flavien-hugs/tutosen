VENV := env
BIN := $(VENV)/bin
SHELL := /bin/bash
MANAGE := python manage.py

include .env

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

update: ## Do apt ugrade and autoremove
	sudo apt update && sudo apt upgrade -y
	sudo apt autoremove -y

.PHONY: ga-env
ga-env: ## Make a new virtual environment
	python3 -m venv $(VENV)
	source $(BIN)/activate
	python3 -m pip install --upgrade pip

.PHONY: ga-install
ga-install: ## Make venv and install requerements
	$(BIN)/pip install --upgrade -r requirements.txt

.PHONY: venv
venv: ## Make a new virtual environment
	pip3 install pipenv
	pipenv shell

.PHONY: install
install: venv ## Install or update dependencies
	pipenv install

freeze: ## Pin current dependencies
	pipenv lock -r > requirements.txt

migrate: ## Make and run migrations
	$(MANAGE) makemigrations
	$(MANAGE) migrate

db-up: ## Pull and start the Docker Postgres container in the background
	docker pull postgres
	docker-compose up -d

db-shell: ## Access the Postgres Docker database interactively with psql. Pass in DBNAME=<name>.
	docker exec -it container_name psql -d $(DBNAME)

.PHONY: test
test: ## Run tests
	$(MANAGE) test honoma --verbosity=0 --parallel --failfast

.PHONY: run
run: ## Run the Django server
	$(MANAGE) runserver

start: install migrate run ## Install requirements, apply migrations, then start development server

createsuperuser: ## Run the Django server
	$(MANAGE) createsuperuser --username="tutosen" --email="flavienhgs@gmail.com"

collectstatic: ## Run collectstatic
	$(MANAGE) collectstatic --no-input

dumpdata:
	$(MANAGE) dumpdata --indent=4 --format=json accounts.user > __backups__/users.json
	$(MANAGE) dumpdata --indent=4 --format=json sites.site > __backups__/sites.json
	$(MANAGE) dumpdata --indent=4 --format=json courses.subject > __backups__/subjects.json
	$(MANAGE) dumpdata --indent=4 --format=json courses.course > __backups__/courses.json
	$(MANAGE) dumpdata --indent=4 --format=json courses.coursechapter > __backups__/lessons.json

loaddata:
	$(MANAGE) loaddata __backups__/users.json
	$(MANAGE) loaddata __backups__/sites.json
