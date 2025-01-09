from fastapi.testclient import TestClient
from mypy_boto3_dynamodb import Client

from tests.mocks.tasks import store_random_task_in_db


def test_delete_task_by_id(api_client: TestClient, dynamo_client: Client) -> None:
    task_instance = store_random_task_in_db(dynamo_client)
    result = api_client.delete(f"/v1/tasks/{task_instance.id}")

    assert result.status_code == 204


def test_delete_task_by_id_not_found(api_client: TestClient, dynamo_client: Client) -> None:
    result = api_client.delete("/v1/tasks/1234")

    assert result.status_code == 404
    assert result.json() == {"detail": "Task not found"}
