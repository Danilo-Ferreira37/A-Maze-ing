PYTHON = python3
VENV = venv
PIP = $(VENV)/bin/pip
PY = $(VENV)/bin/python


run: install
	$(PY) a_maze_ing.py config.txt

install:
	@test -d $(VENV) || $(PYTHON) -m venv $(VENV) > /dev/null
	@$(PIP) install --upgrade pip > /dev/null
	@$(PIP) install flake8 mypy > /dev/null

debug: install
	$(PY) -m pdb a_maze_ing.py config.txt

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@rm -rf mazegen-1.0.0.tar.gz
	@rm -rf mazegen-1.0.0-py3-none-any.whl
	@rm -rf output_maze.txt
	@rm -rf dist

fclean: clean
	@rm -rf venv

lint: install
	@$(VENV)/bin/flake8 .
	@$(VENV)/bin/mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: install
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . --strict

.PHONY: install run debug clean fclean lint lint-strict