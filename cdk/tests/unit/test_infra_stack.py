import aws_cdk as core
import aws_cdk.assertions as assertions
from infra.infra_stack import TaskTrackerStack


def test_lambda_api_created() -> None:
    app = core.App()
    stack = TaskTrackerStack(app, "infra")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties(
        "AWS::DynamoDB::Table",
        {
            "KeySchema": [{"AttributeName": "id", "KeyType": "HASH"}],
            "TableName": "task_tracker",
            "BillingMode": "PAY_PER_REQUEST",
            "SSESpecification": {"SSEEnabled": True},
        },
    )

    template.has_resource_properties(
        "AWS::IAM::Role",
        {
            "RoleName": "TaskTrackerFunctionExecutionRole",
            "AssumeRolePolicyDocument": {
                "Statement": [
                    {
                        "Action": "sts:AssumeRole",
                        "Effect": "Allow",
                        "Principal": {"Service": "lambda.amazonaws.com"},
                    }
                ]
            },
        },
    )

    template.has_resource_properties(
        "AWS::Lambda::Function",
        {
            "Environment": {"Variables": {"aws_region": "ap-southeast-2", "db_table": {}}},
            "Handler": "main.handler",
            "FunctionName": "TaskTrackerAPI",
            "Runtime": "python3.13",
        },
    )

    template.has_resource_properties("AWS::ApiGateway::RestApi", {"Name": "TaskTrackerAPI"})

    template.has_resource_properties(
        "AWS::ApiGateway::Method",
        {
            "HttpMethod": "ANY",
            "Integration": {
                "IntegrationHttpMethod": "POST",
                "Type": "AWS_PROXY",
            },
        },
    )
