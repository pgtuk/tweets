.DEFAULT_GOAL := help

ENV_FILE = .env

help: _help_

_help_:
	@echo make lint - run linters check
	@echo make test - run tests
	@echo make migrate - run migrations
	@echo make run - run linters, test, migrations, then run api and fetching task


migrate:
	alembic upgrade head


lint:
	# All linters ignore src/tweets/migrations directory,
	# because all code there was generated automatically by alembic.

	find src -name "*.py" | xargs pylint --const-rgx=[A-z_]+

	# mypy
	find src -name "*.py" | xargs mypy --config-file=mypy.ini

	# bandit
	bandit -r src

	# safety
	safety check


test:

	if grep -q TESTING $(ENV_FILE) ; then \
		sed -i 's/TESTING=False/TESTING=True/g' $(ENV_FILE) ; \
	else \
		echo "TESTING=True" >> $(ENV_FILE) ; \
	fi

	pytest -s

	sed -i 's/TESTING=True/TESTING=False/g' $(ENV_FILE)


migate:
	alembic upgrade head


run:
	make lint
	# make test

	make migrate

	python src/tweets/fetch.py &
	uvicorn src.api:Api --host 0.0.0.0 --port 5000
	