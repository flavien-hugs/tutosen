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

start: install migrate run ## Install requirements, apply migrations, then start development server

createsuperuser: ## Run the Django server
	$(MANAGE) createsuperuser --email="unste.inc@pm.me"

changepassword: ## Change password superuser
	$(MANAGE) changepassword unste.inc@pm.me

collectstatic: ## Run collectstatic
	$(MANAGE) collectstatic --noinput

dumpdata: ## dump data
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes --format=json accounts.user > __backups__/users.json
	$(MANAGE) dumpdata --indent=4 --format=json sites.site > __backups__/sites.json
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes  --format=json courses.subject > __backups__/subjects.json
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes  --format=json courses.course > __backups__/courses.json
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes  --format=json courses.coursechapter > __backups__/lessons.json

loaddata: ## load data
	$(MANAGE) loaddata __backups__/users.json
	$(MANAGE) loaddata __backups__/sites.json
	$(MANAGE) loaddata __backups__/subjects.json
	$(MANAGE) loaddata __backups__/courses.json
	$(MANAGE) loaddata __backups__/lessons.json
