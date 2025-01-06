from fastapi.testclient import TestClient


def test_get_all_tasks(api_client: TestClient) -> None:
    result = api_client.get("/v1/tasks")

    assert result.status_code == 200
    assert result.json() == []
