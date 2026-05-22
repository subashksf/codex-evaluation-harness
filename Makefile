.PHONY: install format lint typecheck test ci

PYTHON ?= python3.11
VENV ?= .venv
VENV_PYTHON := $(VENV)/bin/python

install:
	$(PYTHON) -m venv $(VENV)
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install -e ".[dev]"

format:
	$(VENV_PYTHON) -m ruff check --fix .
	$(VENV_PYTHON) -m ruff format .

lint:
	$(VENV_PYTHON) -m ruff check .
	$(VENV_PYTHON) -m ruff format --check .

typecheck:
	$(VENV_PYTHON) -m mypy src tests

test:
	$(VENV_PYTHON) -m pytest

ci: lint typecheck test
