include Makefile.variables.mk


.PHONY: setup
setup:
	$(call log, setting up everything)
	$(PYTHON) $(DIR_SCRIPTS)/setup_pycharm.py


.PHONY: format
format:
	$(call log, reorganizing imports & formatting code)
	$(RUN) isort --virtual-env="$(DIR_VENV)" "$(DIR_SRC)" "$(DIR_TESTS)" "$(DIR_SCRIPTS)"
	$(RUN) black "$(DIR_SRC)" "$(DIR_TESTS)" "$(DIR_SCRIPTS)"


.PHONY: run
run:
	$(call log, starting django server)
	$(PYTHON) src/manage.py runserver


.PHONY: test
test:
	$(call log, running tests)
	$(RUN) pytest .
	$(RUN) isort --virtual-env="$(DIR_VENV)" --check-only "$(DIR_SRC)" "$(DIR_TESTS)" "$(DIR_SCRIPTS)"
	$(RUN) black --check "$(DIR_SRC)" "$(DIR_TESTS)" "$(DIR_SCRIPTS)"


.PHONY: migrate
migrate:
	$(call log, applying migrations)
	$(PYTHON) src/manage.py migrate


.PHONY: migrations
migrations:
	$(call log, generating migrations)
	$(PYTHON) src/manage.py makemigrations


.PHONY: su
su:
	$(call log, creating a new superuser)
	$(PYTHON) src/manage.py createsuperuser


.PHONY: sh
sh:
	$(call log, starting django shell)
	$(PYTHON) src/manage.py shell


.PHONY: static
static:
	$(call log, collecting static)
	$(PYTHON) src/manage.py collectstatic --no-input


.PHONY: resetdb
resetdb:  dropdb createdb migrations migrate
	$(call log, resetting db to initial state)


.PHONY: dropdb
dropdb:
	$(call log, dropping database)
	psql -d postgres -c "DROP DATABASE IF EXISTS \"$(shell $(PYTHON) $(DIR_SCRIPTS)/get_db_name.py)\";"


.PHONY: createdb
createdb:
	$(call log, creating database)
	psql -d postgres -c "CREATE DATABASE \"$(shell $(PYTHON) $(DIR_SCRIPTS)/get_db_name.py)\";"


.PHONY: venv
venv:
	$(call log, installing packages for venv)
	@$(PIPENV_INSTALL)


.PHONY: venv-dev
venv-dev:
	$(call log, installing dev packages for venv)
	@$(PIPENV_INSTALL) --dev
