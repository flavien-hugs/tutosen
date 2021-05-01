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
	$(MANAGE) dumpdata --indent=4 --format=json accounts.user > __backups__/users.json
	$(MANAGE) dumpdata --indent=4 --format=json sites.site > __backups__/sites.json
	$(MANAGE) dumpdata --indent=4 --format=json pages.aboutus > __backups__/page_aboutus.json
	$(MANAGE) dumpdata --indent=4 --format=json pages.pagecgu > __backups__/page_cgu.json
	$(MANAGE) dumpdata --indent=4 --format=json pages.pagesupport > __backups__/page_upport.json

loaddata:
	$(MANAGE) loaddata __backups__/users.json
	$(MANAGE) loaddata __backups__/sites.json

test-deploy:
	$(MANAGE) check --deploy

deploy:
	$(MANAGE) collectstatic
	$(MANAGE) makemigrations
	$(MANAGE) migrate
	$(MANAGE) loaddata
