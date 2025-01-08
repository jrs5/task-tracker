import pytest
from fastapi.testclient import TestClient
from mypy_boto3_dynamodb import Client

from task_tracker.contract import spec
from tests.mocks.tasks import store_random_task_in_db


def test_get_all_tasks_empty_table(api_client: TestClient, dynamo_client: Client) -> None:
    result = api_client.get("/v1/tasks")

    assert result.status_code == 200
    assert result.json() == []


def test_get_all_tasks_single_item(api_client: TestClient, dynamo_client: Client) -> None:
    task_instance = store_random_task_in_db(dynamo_client)
    result = api_client.get("/v1/tasks")

    task_result = spec.Task(**result.json()[0])

    assert result.status_code == 200
    assert task_instance.id == task_result.id
    assert task_instance.title == task_result.title
    assert task_instance.description == task_result.description
    assert task_instance.due_date == task_result.due_date


def test_get_all_tasks_multiple_items(api_client: TestClient, dynamo_client: Client) -> None:
    total_tasks = 10
    for i in range(total_tasks):
        store_random_task_in_db(dynamo_client)

    result = api_client.get("/v1/tasks")

    task_results = [spec.Task(**task) for task in result.json()]

    assert result.status_code == 200
    assert len(task_results) == total_tasks


@pytest.mark.parametrize(
    "completed, total_tasks",
    [(True, 2), (False, 1)],
)
def test_get_completed_tasks(api_client: TestClient, dynamo_client: Client, completed: bool, total_tasks: int) -> None:
    store_random_task_in_db(dynamo_client, completed=True)
    store_random_task_in_db(dynamo_client, completed=True)
    store_random_task_in_db(dynamo_client, completed=False)

    result = api_client.get(f"/v1/tasks?completed={completed}")

    task_results = [spec.Task(**task) for task in result.json()]

    assert result.status_code == 200
    assert len(task_results) == total_tasks
