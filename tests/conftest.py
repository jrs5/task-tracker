from collections.abc import Generator
from dataclasses import dataclass

import boto3
import pytest
from fastapi.testclient import TestClient
from moto import mock_aws
from mypy_boto3_dynamodb import Client as DynamoDBClient

from main import app
from task_tracker.config import get_config


@dataclass
class LambdaContext:
    function_name: str = "tests"
    memory_limit_in_mb: int = 128
    invoked_function_arn: str = "arn:aws:lambda:ap-southeast-2:123456789012:function:tests"
    aws_request_id: str = "da658bd3-2d6f-4e7b-8ec2-937234644fdc"


@pytest.fixture
def lambda_context() -> LambdaContext:
    return LambdaContext()


@pytest.fixture
def api_client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def dynamo_client() -> Generator[DynamoDBClient, None, None]:
    config = get_config()
    with mock_aws():
        client = boto3.client("dynamodb", region_name=config.aws_region)
        client.create_table(
            TableName=config.db_table,
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )
        yield client
