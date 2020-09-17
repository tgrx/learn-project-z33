HERE := $(shell pwd)
VENV := $(shell pipenv --venv)
SRC := ${HERE}

RUN := pipenv run
PY := ${RUN} python


.PHONY: format
format:
	${RUN} isort --virtual-env "${VENV}" "${SRC}"
	${RUN} black "${SRC}"


.PHONY: run
run:
	${PY} -m app


.PHONY: test
test:
	${RUN} pytest .


.PHONY: wipe
wipe:
	rm -rf "${HERE}/.pytest_cache"
	rm -rf "${HERE}/storage"/*.json
	rm -rf "${HERE}/storage"/*.txt
	rm -rf "${HERE}/tests/functional/artifacts"/*.html
	rm -rf "${HERE}/tests/functional/artifacts"/*.png


.PHONY: venv
venv:
	pipenv install


.PHONY: venv-dev
venv-dev:
	pipenv install --dev
