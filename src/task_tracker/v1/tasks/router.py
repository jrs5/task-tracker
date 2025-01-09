from http import HTTPStatus
from typing import Annotated, Any
from uuid import uuid4

from fastapi import Body, HTTPException, Path, Query, Request, Response

from task_tracker import db
from task_tracker.config import get_config
from task_tracker.contract import spec
from task_tracker.fastapi_utils import LoggedRouter

router = LoggedRouter()


@router.get(
    "/",
    response_model=spec.GetTasks,
    summary="Retrieve a list of tasks. Optionally, filter by completion status",
)
def get_all_tasks(completed: Annotated[bool | None, Query()] = None) -> spec.GetTasks:
    config = get_config()
    tasks = db.get_tasks(config.db_table, config.aws_region)
    if completed is None:
        return spec.GetTasks(data=tasks)

    return spec.GetTasks(data=[task for task in tasks if task.completed == completed])


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


@router.get(
    "/{id}",
    response_model=spec.Task,
    summary="Retrieve details of a specific task by its unique ID.",
)
def get_task_by_id(
    id: Annotated[str, Path],
) -> spec.Task:
    config = get_config()

    task = db.get_task_by_id(id, config.db_table, config.aws_region)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.put(
    "/{id}",
    response_model=spec.Task,
    summary="Update an existing task",
)
def update_task_by_id(
    id: Annotated[str, Path],
    body: Annotated[spec.TaskUpdate, Body],
) -> spec.Task:
    config = get_config()

    task = db.get_task_by_id(id, config.db_table, config.aws_region)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    updated_task = spec.Task(
        id=task.id,
        title=body.title if body.title else task.title,
        description=body.description if body.description else task.description,
        due_date=body.due_date if body.due_date else task.due_date,
        completed=body.completed if body.completed else task.completed,
        priority=body.priority if body.priority else task.priority,
    )
    db.store_task(updated_task, config.db_table, config.aws_region)

    return updated_task
