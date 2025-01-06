from typing import Annotated

from fastapi import Query

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
