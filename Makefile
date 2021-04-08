SHELL := /bin/bash
MANAGE := python manage.py

TEST_SETTINGS := test

.PHONY: all help deps static migrate restart update deploy

all: help

help:
	@echo "Usage:"
	@echo "  make deploy - pull and deploy the update"
	@echo "  make test - run automated tests"

pip-install:
	pip install -r requirements.txt

pipenv-install:
	pipenv install

generate-requirement:
	pipenv lock -r > requirements.txt

migratedb:
	$(MANAGE) makemigrations
	$(MANAGE) migrate

createsuperuser:
	$(MANAGE) createsuperuser --username='tutosen' --email='contact@tutosen.com'
	
collectstatic:
	$(MANAGE) collectstatic

dumpdata:
	$(MANAGE) dumpdata --format=json user.user > __backups__/users.json

loaddata:
	$(MANAGE) loaddata __backups__/users.json


test-deploy:
	$(MANAGE) check --deploy

deploy:
	$(MANAGE) collectstatic
	$(MANAGE) makemigrations
	$(MANAGE) migrate
	$(MANAGE) loaddata
