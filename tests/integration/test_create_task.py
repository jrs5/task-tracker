from fastapi.testclient import TestClient
from mypy_boto3_dynamodb import Client

from task_tracker.contract import spec


def test_create_task(api_client: TestClient, dynamo_client: Client) -> None:
    data = {
        "title": "test",
        "description": "test",
        "dueDate": "2025-01-01T00:00:00.000Z",
        "priority": "low",
    }
    result = api_client.post("/v1/tasks", json=data)
    new_task = spec.Task(**result.json())

    assert result.status_code == 201
    assert new_task.completed is False
