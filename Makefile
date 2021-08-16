.DEFAULT_GOAL := build

install: # Install dependencies
	flit install --deps develop --symlink

fmt format: # Run code formatters
	isort --profile black .
	black .

lint: # Run code linters
	isort --profile black --check --diff .
	black --check --diff --color .
	flake8 --max-line-length 88 --max-complexity 8 --select C,E,F,W,B,B950,S --ignore E203,E501 ninja_apikey
	mypy --strict ninja_apikey/security.py

test: # Run tests
	pytest --ds=sample_project.settings -v sample_project ninja_apikey/tests.py

cov test-cov: # Run tests with coverage
	pytest --ds=sample_project.settings --cov=ninja_apikey --cov-report=term-missing --cov-report=xml -v sample_project ninja_apikey/tests.py

build: # Build project
	make install
	make lint
	make cov
