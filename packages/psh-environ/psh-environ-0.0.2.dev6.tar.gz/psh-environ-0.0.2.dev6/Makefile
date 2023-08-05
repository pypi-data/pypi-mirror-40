ifeq ($(VIRTUAL_ENV), )
VIRTUAL_ENV := $(shell pipenv --venv 2>/dev/null)
endif

ifeq ($(VIRTUAL_ENV), )
VIRTUAL_ENV := $(CURDIR)/.venv
endif

PYTHON ?= $(VIRTUAL_ENV)/bin/python
python_code := psh_environ ci tests

help:
	@echo 'Usage: make <target>'
	@echo '  Where <target> is one of:'
	@echo '    all             Execute all build operations.'
	@echo '    clean           Delete the generated output.'
	@echo '    debug-make      Print all of the `make` variables for debugging.'
	@echo '    format          Execute black and isort formatters on python code.'
	@echo '    format-pipfile  Reformats the project Pipfile using the format-pipfile script.
	@echo '    help            Show this message and exit.'
	@echo '    lock            Regenerate the lockfile.'
	@echo '    sync            Synchronize the virtual environment with the lockfile.'
	@echo '    test            Executes py.test unit tests.'

debug-make:
	@echo "CURDIR      := $(CURDIR)"
	@echo "VIRTUAL_ENV := $(VIRTUAL_ENV)"
	@echo "PYTHON      := $(PYTHON)"
	@echo "python_code := $(python_code)"

Pipfile.lock: Pipfile
	pipenv lock --pre

all: lock sync format test

clean:
	git clean -xdf -e .env -e .venv

format: format-pipfile $(PYTHON)
	$(PYTHON) ci/bootstrap.py
	$(PYTHON) -m isort --recursive $(python_code)
	$(PYTHON) -m black $(python_code)

format-pipfile:
	$(PYTHON) -m format_pipfile -r $(CURDIR)/requirements.txt -p $(CURDIR)/Pipfile

lock: Pipfile.lock

sync $(PYTHON): Pipfile.lock
	pipenv sync --dev
	pipenv clean
	@touch $(PYTHON)

test: $(PYTHON)
	$(PYTHON) -m pytest

.PHONY: all clean debug-make format help lock sync test
