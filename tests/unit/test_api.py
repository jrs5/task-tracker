from fastapi.testclient import TestClient


def test_api_ping(api_client: TestClient) -> None:
    result = api_client.get("/ping")

    assert result.status_code == 200
    assert result.json() == "pong"


def test_openapi_json(api_client: TestClient) -> None:
    response = api_client.get("/openapi.json")
    assert response.status_code == 200
