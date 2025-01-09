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


def get_tasks(table: str, region: str) -> list[spec.Task]:
    """Get all tasks from DynamoDB

    Args:
        table (str): DynamoDB table name
        region (str): AWS Region

    Returns:
        list[spec.Task]: A list of tasks
    """
    dynamodb = boto3.client("dynamodb", region_name=region)

    # TODO: Project is small and scanning is ok for a small table
    # Use query once multiple users are added to the schema
    response = dynamodb.scan(TableName=table)

    tasks: list[spec.Task] = []
    for item in response["Items"]:
        tasks.append(spec.Task(**deserialize_item(item)))

    return tasks


def get_task_by_id(id: str, table: str, region: str) -> spec.Task | None:
    """Get a task by id from DynamoDB

    Args:
        id (str): unique id
        table (str): DynamoDB table name
        region (str): AWS Region

    Returns:
        spec.Task if id is found, otherwise None
    """
    dynamodb = boto3.client("dynamodb", region_name=region)
    response = dynamodb.query(
        TableName=table,
        KeyConditionExpression="id = :id_value",
        ExpressionAttributeValues={
            ":id_value": {"S": id},
        },
    )

    if response["Count"] == 0:
        return None

    return spec.Task(**deserialize_item(response["Items"][0]))
