import aws_cdk as core
import aws_cdk.assertions as assertions
from infra.infra_stack import TaskTrackerStack


def test_lambda_api_created() -> None:
    app = core.App()
    stack = TaskTrackerStack(app, "infra")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties(
        "AWS::Lambda::Function",
        {
            "Environment": {"Variables": {}},
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
