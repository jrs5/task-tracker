from fastapi.testclient import TestClient
from mypy_boto3_dynamodb import Client

from task_tracker.contract import spec
from tests.mocks.tasks import store_random_task_in_db


def test_update_task_by_id(api_client: TestClient, dynamo_client: Client) -> None:
    task_instance = store_random_task_in_db(dynamo_client)
    data = {
        "title": "updated_title",
        "description": "updated_description",
        "dueDate": "2025-01-01T00:00:00.000Z",
        "priority": "high",
    }

    result = api_client.put(f"/v1/tasks/{task_instance.id}", json=data)

    task_result = spec.Task(**result.json())

    assert result.status_code == 200
    assert task_result.id == task_instance.id
    assert task_result.title == "updated_title"
    assert task_result.description == "updated_description"
    assert task_result.priority == spec.Priority.high


def test_update_task_by_id_not_found(api_client: TestClient, dynamo_client: Client) -> None:
    data = {"title": "test"}
    result = api_client.put("/v1/tasks/1234", json=data)

    assert result.status_code == 404
    assert result.json() == {"detail": "Task not found"}


def test_update_task_by_id_invalid_body(api_client: TestClient, dynamo_client: Client) -> None:
    task_instance = store_random_task_in_db(dynamo_client)
    data = {"priority": "invalid"}

    result = api_client.put(f"/v1/tasks/{task_instance.id}", json=data)
    error = result.json()["detail"][0]

    assert result.status_code == 422
    assert error["ctx"] == {"expected": "'low', 'medium' or 'high'"}


def test_update_task_by_id_no_body(api_client: TestClient, dynamo_client: Client) -> None:
    task_instance = store_random_task_in_db(dynamo_client)

    result = api_client.put(f"/v1/tasks/{task_instance.id}")
    error = result.json()["detail"][0]

    assert result.status_code == 422
    assert error == {"type": "missing", "loc": ["body"], "msg": "Field required", "input": None}
