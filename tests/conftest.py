from dataclasses import dataclass

import pytest
from fastapi.testclient import TestClient

from main import app


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
