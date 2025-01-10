# Task Tracker API

A simple API to manage personal tasks or to-do lists with FastAPI

## Getting started

The `pyproject.toml` file is configured for Python3.13, make sure that `python3` command is configured for Python3.13, alternatively, adjust the command below to create the virtual environment for Python3.13

Run the following commands to start developing in this repository:

```bash
git clone git@github.com:jrs5/task-tracker.git
python3 -m venv venv
source venv/bin/activate
make bootstrap
```

This will:

- Clone the repository
- Create and activate Python virtual environment
- Install all dependencies using Poetry
- Configure all the necessary tools to begin development

## Local development

`Makefile` has a bunch of commands to apply code quality checks more easily

`ruff` is used for linting and formatting

```bash
make format
```

`mypy` is used for type checking

```bash
make check
```

`pytest` is used for unit tests

```bash
make test-app
```

All commands have been wrapped into a single command that formats, lint checks, type checks and tests the app.

```bash
make all-dev
```

Infrastructure is developed using AWS CDK. Unit tests for infra are in a separate folder and are run with a separate make command

```bash
make all-dev-plus-cdk
```

`pre-commit` is used to guarantee that all commits pass format, lint and type checks.

## Local Testing

- Update all required environment variables in the `.env` file
- Use the `run` command in the `Makefile` to start a local server

```bash
make run
```

- Once the server is running, open your browser and enter `localhost:8000/docs` to check OpenAPI spec

## CI

Once a feature has been tested locally, the feature branch can be pushed to GitHub. Then, a Pull Request can be raised to merge the feature to `main` branch. This will trigger an automated GitHub action workflow to run Python checks and unit tests for both app and infrastructure. There is a protection rule to merge to `main` only after the GitHub action job is successful

## Deployment

The Infrastructure is created as IaC using AWS CDK. All the infrastructure related code is stored inside `cdk/` folder.

- Assume a role with enough permissions to create resources in the target account and region
- Make sure the AWS account is bootstrapped with AWS CDK (one-time step) using the CDK CLI
- Use the `deploy` command in the `Makefile`. This will package the app into a zip file and then deploy automatically to the target AWS account

```bash
make deploy
```

## Invoke the API

- Make sure to use the `x-api-key` header with the API key deployed and attached to the correct Usage Plan.
