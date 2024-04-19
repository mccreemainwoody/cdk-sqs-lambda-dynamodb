import aws_cdk as core
import aws_cdk.assertions as assertions
import pytest

from cdk_sqs_lambda_dynamodb.stacks import SrcStack


@pytest.fixture
def template():
    app = core.App()
    stack = SrcStack(app, "src")
    return assertions.Template.from_stack(stack)


def test_sqs_queue_created(template):
    template.has_resource_properties("AWS::SQS::Queue", {
        "VisibilityTimeout": 300
    })


def test_sns_topic_created(template):
    template.resource_count_is("AWS::SNS::Topic", 1)
