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

`ruff` is used for linting and formatting

`mypy` is used for type checking

`pytest` is used for unit tests

## Local Testing

- Update all required environment variables in the `.env` file
- Use the `run` command in the `Makefile` to start a local server

```bash
make run
```

- Once the server is running, open your browser and enter `localhost:8000/docs` to check OpenAPI spec
