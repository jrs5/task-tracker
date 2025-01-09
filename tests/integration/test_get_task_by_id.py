from fastapi.testclient import TestClient
from mypy_boto3_dynamodb import Client

from task_tracker.contract import spec
from tests.mocks.tasks import store_random_task_in_db


def test_get_task_by_id_not_found(api_client: TestClient, dynamo_client: Client) -> None:
    result = api_client.get("/v1/tasks/1234")

    assert result.status_code == 404
    assert result.json() == {"detail": "Task not found"}


def test_get_task_by_id(api_client: TestClient, dynamo_client: Client) -> None:
    task_instance = store_random_task_in_db(dynamo_client)
    result = api_client.get(f"/v1/tasks/{task_instance.id}")

    task_result = spec.Task(**result.json())

    assert result.status_code == 200
    assert task_instance.id == task_result.id
    assert task_instance.title == task_result.title
    assert task_instance.description == task_result.description
    assert task_instance.due_date == task_result.due_date
