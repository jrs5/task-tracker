from mypy_boto3_dynamodb import Client
from polyfactory.factories.pydantic_factory import ModelFactory

from task_tracker import db
from task_tracker.config import get_config
from task_tracker.contract import spec


class TaskFactory(ModelFactory[spec.Task]): ...


def store_random_task_in_db(dynamo_client: Client, completed: bool = False) -> spec.Task:
    task_instance = TaskFactory.build()
    config = get_config()
    task_instance.completed = completed
    db.store_task(task_instance, config.db_table, config.aws_region)
    return task_instance
