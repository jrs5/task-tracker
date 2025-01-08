### Python scripts ###

## Bootstrap target to configure a cloned repository for first use
.PHONY: bootstrap
bootstrap: ensure-poetry install install-dev install-pre-commit

.PHONY: install
install:
	@echo ">> Installing dependencies"
	poetry install --without dev

## Install for development
.PHONY: install-dev
install-dev: ensure-poetry install
	@echo ">> Installing dev dependencies"
	poetry install --only dev

## Install pre commit hooks
.PHONY: install-pre-commit
install-pre-commit:
	@echo ">> Installing pre-commit"
	poetry run python -m pip install pre-commit
	poetry run pre-commit install
	poetry run pre-commit run --all-files

## Lint and format checks using ruff
.PHONY: ruff
ruff:
	poetry run ruff check .
	poetry run ruff format --check .

## Fix lint and format files using ruff
.PHONY: format
format:
	poetry run ruff check . --fix
	poetry run ruff format .

## Type check using dmypy
.PHONY: mypy
mypy:
	poetry run dmypy run -- .

## Run checks (ruff + mypy)
.PHONY: check
check: ruff mypy

# Run all for dev
.PHONY: all-dev
all-dev: format ruff mypy test-app

.PHONY: all-dev-plus-cdk
all-dev-plus-cdk: format ruff mypy test-all

### Unit Tests
.PHONY: test-all
test-all: test-app test-cdk

.PHONY: test-app
test-app:
	poetry run coverage run -m pytest tests
	poetry run coverage report

.PHONY: test-cdk
test-cdk: package
	poetry run coverage run -m pytest cdk/tests
	poetry run coverage report

.PHONY: show-outdated
show-outdated:
	poetry show --outdated

.PHONY: ensure-poetry
ensure-poetry:
	@pip install --quiet poetry

.PHONY: run
run: ensure-poetry
	cd src && poetry run python -m run

# Package
.PHONY: package
package: ensure-poetry
	pip --version
	mkdir -p build
	poetry export --directory=. --format requirements.txt --without-hashes --output=build/requirements.txt
	pip install --target=dist -r build/requirements.txt --platform=manylinux2014_x86_64 --only-binary=:all:

	cp -rf src/* dist/
	cd dist && zip -r package.zip .
	mv dist/package.zip cdk/package.zip
