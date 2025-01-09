import os
from pathlib import Path
from typing import Any

from aws_cdk import Duration, RemovalPolicy, Stack
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as lambda_
from constructs import Construct
from dotenv import load_dotenv

load_dotenv()


class TaskTrackerStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs: Any) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create the DynamoDB table
        table = dynamodb.Table(
            self,
            id="TaskTrackerTable",
            table_name="task_tracker",
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING,
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            encryption=dynamodb.TableEncryption.AWS_MANAGED,
            removal_policy=RemovalPolicy.DESTROY,
        )

        # Create the IAM role for Lambda
        lambda_role = iam.Role(
            self,
            "TaskTrackerFunctionExecutionRole",
            role_name="TaskTrackerFunctionExecutionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
            ],
        )

        lambda_role.add_to_policy(
            iam.PolicyStatement(
                actions=["dynamodb:*"],
                resources=[table.table_arn],
            )
        )

        # Lambda Function for FastAPI entrypoint handler
        # asset logic is required to handle both unit tests and cdk synth
        asset = Path(".")
        asset = asset.joinpath("package.zip") if asset.absolute().stem == "cdk" else asset.joinpath("cdk/package.zip")

        task_tracker_function = lambda_.Function(
            self,
            id="TaskTrackerFunction",
            runtime=lambda_.Runtime.PYTHON_3_13,
            code=lambda_.Code.from_asset(str(asset)),
            function_name="TaskTrackerAPI",
            handler="main.handler",
            memory_size=256,
            role=lambda_role,
            timeout=Duration.seconds(10),
            environment={
                "aws_region": os.environ.get("AWS_REGION", "ap-southeast-2"),
                "db_table": table.table_name,
                "environment": os.environ.get("ENVIRONMENT", "DEV"),
                "log_level": os.environ.get("LOG_LEVEL", "INFO"),
            },
        )

        # API Gateway resource
        api = apigateway.LambdaRestApi(
            self,
            id="TaskTrackerAPI",
            handler=task_tracker_function,
            proxy=False,
        )

        # Proxy resource with a ANY method for FastAPI
        api_resource = api.root.add_resource("{proxy+}")
        api_resource.add_method("ANY", api_key_required=True)

        # Create an API Key
        api_key = apigateway.ApiKey(
            self,
            id="TaskTrackerApiKey",
            api_key_name="TaskTrackerApiKey",
            description="TaskTracker API Key for accessing the Lambda service",
            enabled=True,
        )

        # Create a Usage Plan for the API Key
        plan = api.add_usage_plan(
            "TaskTrackerUsagePlan",
            name="TaskTrackerUsagePlan",
            throttle=apigateway.ThrottleSettings(
                rate_limit=10,
                burst_limit=20,
            ),
            quota=apigateway.QuotaSettings(
                limit=1000,
                period=apigateway.Period.MONTH,
            ),
        )
        plan.add_api_key(api_key)

        # Link the usage plan to the API Gateway stage
        plan.add_api_stage(stage=api.deployment_stage)
