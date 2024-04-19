import aws_cdk.assertions as assertions
import pytest

from aws_cdk import (
    App,
    aws_sqs as sqs,
    aws_dynamodb as dynamodb,
)

from cdk_sqs_lambda_dynamodb.stacks import SqsLambdaDynamoDB


@pytest.fixture
def stack():
    return SqsLambdaDynamoDB(App(), "SqsLambdaDynamoDB")


@pytest.fixture
def template(stack) -> assertions.Template:
    return assertions.Template.from_stack(stack)


@pytest.fixture
def queue(stack) -> sqs.Queue:
    return stack.node.find_child("Queue")


@pytest.fixture
def dead_letter_queue(stack) -> sqs.Queue:
    return stack.node.find_child("QueueDeadLetterQueue")


@pytest.fixture
def table(stack) -> dynamodb.Table:
    return stack.node.find_child("Table")


def test_sqs_queue_has_dead_letter_queue(stack, template, dead_letter_queue):
    template.has_resource_properties(
        "AWS::SQS::Queue",
        {
            "FifoQueue": True,
            "RedrivePolicy": {
                "deadLetterTargetArn": stack.resolve(
                    dead_letter_queue.queue_arn
                ),
                "maxReceiveCount": 10,
            },
        },
    )


def test_lambda_function_has_correct_env_variable(stack, template, table):
    template.has_resource_properties(
        "AWS::Lambda::Function",
        {
            "Environment": {
                "Variables": {
                    "TABLE_NAME": stack.resolve(table.table_name),
                },
            },
        },
    )


def test_dynamodb_table_has_correct_schema(template):
    template.has_resource_properties(
        "AWS::DynamoDB::Table",
        {
            "KeySchema": [
                {"AttributeName": "id", "KeyType": "HASH"},
                {"AttributeName": "timestamp", "KeyType": "RANGE"},
            ],
            "AttributeDefinitions": [
                {"AttributeName": "id", "AttributeType": "S"},
                {"AttributeName": "timestamp", "AttributeType": "S"},
            ],
        },
    )


def test_lambda_function_is_subscribed_to_sqs_queue(stack, template, queue):
    template.has_resource_properties(
        "AWS::Lambda::EventSourceMapping",
        {
            "EventSourceArn": stack.resolve(queue.queue_arn)
        },
    )
