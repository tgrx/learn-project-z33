include ./Makefile.variables.mk


.PHONY: format
format:
	$(call log, rearranging imports and making code black)
	$(RUN) isort --virtual-env "$(VENV_DIR)" "$(SRC_DIR)"
	$(RUN) isort --virtual-env "$(VENV_DIR)" "$(TESTS_DIR)"
	$(RUN) black "$(SRC_DIR)"
	$(RUN) black "$(TESTS_DIR)"


.PHONY: run
run: export PYTHONPATH = $(SRC_DIR)
run:
	$(call log, running development web server)
	$(PY) -m app


.PHONY: test
test:
	$(call log, running tests)
	$(RUN) pytest .


.PHONY: wipe
wipe:
	$(call log, wiping garbage)
	rm -rf "$(PROJECT_DIR)/.pytest_cache"
	rm -rf "$(PROJECT_DIR)/storage"/*.json
	rm -rf "$(PROJECT_DIR)/storage"/*.txt
	rm -rf "$(PROJECT_DIR)/tests/functional/artifacts"/*.html
	rm -rf "$(PROJECT_DIR)/tests/functional/artifacts"/*.png


.PHONY: venv
venv:
	$(call log, installing packages for venv)
	@$(PIPENV_INSTALL)


.PHONY: venv-dev
venv-dev:
	$(call log, installing dev packages for venv)
	@$(PIPENV_INSTALL) --dev
