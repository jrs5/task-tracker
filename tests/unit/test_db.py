from typing import Any

import pytest
from mypy_boto3_dynamodb import Client

from task_tracker import db
from task_tracker.config import get_config
from task_tracker.contract import spec


@pytest.fixture
def json_item() -> dict:
    return {
        "customer_id": "123",
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30,
    }


def test_dynamo_item_deserialization(json_item: dict) -> None:
    dynamo_item = {
        "customer_id": {"S": json_item["customer_id"]},
        "name": {"S": json_item["name"]},
        "email": {"S": json_item["email"]},
        "age": {"N": json_item["age"]},
    }

    deserialized_item = db.deserialize_item(dynamo_item)
    assert deserialized_item == json_item


def test_dynamo_item_deserialization_normal_json(json_item: dict) -> None:
    deserialized_item = db.deserialize_item(json_item)
    assert deserialized_item == json_item


def test_store_task(dynamo_client: Client) -> None:
    config = get_config()
    id = "123"
    data: dict[str, Any] = {
        "id": id,
        "title": "test",
        "description": "test",
        "dueDate": "2025-01-01T00:00:00.000Z",
        "priority": "low",
        "completed": False,
    }

    assert db.store_task(spec.Task(**data), config.db_table, config.aws_region)

    # assert task is stored in DynamoDB
    response = dynamo_client.get_item(TableName=config.db_table, Key={"id": {"S": id}})

    item = db.deserialize_item(response["Item"])
    assert item["title"] == item["description"] == "test"
    assert item["priority"] == "low"
