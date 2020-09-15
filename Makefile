HERE := $(shell pwd)
VENV := $(shell pipenv --venv)
SRC := ${HERE}/src
PYTHONPATH := ${SRC}

RUN := pipenv run
PY := ${RUN} python


.PHONY: format
format:
	${RUN} isort --virtual-env "${VENV}" "${HERE}/src"
	${RUN} black "${HERE}/src"


.PHONY: run
run:
	PYTHONPATH="${PYTHONPATH}" ${PY} -m app


.PHONY: wipe
	rm -rf "${HERE}/.pytest_cache"
	rm -rf "${HERE}/storage/*.txt"
