from http import HTTPStatus
from typing import Annotated, Any
from uuid import uuid4

from fastapi import Body, Query, Request, Response

from task_tracker import db
from task_tracker.config import get_config
from task_tracker.contract import spec
from task_tracker.fastapi_utils import LoggedRouter

router = LoggedRouter()


@router.get(
    "/",
    response_model=list[spec.Task],
    summary="Retrieve a list of tasks. Optionally, filter by completion status",
)
def get_all_tasks(completed: Annotated[str | None, Query()] = None) -> list[spec.Task]:
    # TODO: Get tasks from DB
    return []


@router.post(
    "/",
    response_model=spec.Task,
    status_code=HTTPStatus.CREATED,
    summary="Create a new task",
)
def create_task(
    body: Annotated[spec.TaskCreate, Body],
    request: Request,
    response: Response,
) -> spec.Task:
    config = get_config()

    new_task_input: dict[str, Any] = body.model_dump()
    new_task_input.update({"id": str(uuid4())})
    new_task = spec.Task(**new_task_input)

    db.store_task(new_task, config.db_table, config.aws_region)

    return new_task
