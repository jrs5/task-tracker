from datetime import UTC, datetime
from typing import Any

import boto3
from boto3.dynamodb.types import TypeDeserializer

from task_tracker.contract import spec


def deserialize_item(items: dict[str, Any]) -> dict[str, Any]:
    deserializer = TypeDeserializer()
    try:
        return {key: deserializer.deserialize(value) for key, value in items.items()}
    except Exception:
        return items


def store_task(task: spec.Task, table: str, region: str) -> bool:
    """Store a task in DynamoDB

    Args:
        task (spec.Task): Task to store in DB
        table (str): DynamoDB table name
        region (str): AWS Region

    Returns:
        bool: Bool to indicate if the token was stored correctly
    """
    dynamodb = boto3.client("dynamodb", region_name=region)
    response = dynamodb.put_item(
        TableName=table,
        Item={
            "id": {"S": task.id},
            "title": {"S": task.title},
            "description": {"S": task.description},
            "due_date": {"S": task.due_date.isoformat()},
            "priority": {"S": task.priority.value if task.priority else spec.Priority.low.value},
            "completed": {"BOOL": task.completed},
            "timestamp": {"N": str(int(datetime.now(UTC).timestamp()))},
        },
    )
    return response["ResponseMetadata"]["HTTPStatusCode"] == 200
