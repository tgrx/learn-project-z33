# -----------------------------------------------
# independent variables

VENV_DIR := $(shell pipenv --venv)


# -----------------------------------------------
# OS-depend variables

ifeq ($(OS), Windows_NT)
	PROJECT_DIR := $(shell cd)
else
	PROJECT_DIR := $(shell pwd)
endif


# -----------------------------------------------
# Virtualenv-depend variables

ifeq ($(shell python -m detect_venv), True)
	IN_VENV := True
	RUN :=
	PIPENV_INSTALL := echo Cannot create venv under venv
else
	IN_VENV := False
	RUN := pipenv run
	PIPENV_INSTALL := pipenv install
endif


# -----------------------------------------------
# calculated variables

PY := $(RUN) python
SRC_DIR := $(PROJECT_DIR)/src


# -----------------------------------------------
# functions

define log
	@tput bold; tput setab 0; tput setaf 4; echo ">>>>>>>>>>>>>>>>    $(1)    "; tput sgr0;
endef
