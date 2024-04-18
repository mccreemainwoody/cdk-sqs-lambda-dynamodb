import aws_cdk as cdk
import aws_cdk.assertions as assertions

from cdk.stacks.demo_sqs_lambda_dynamodb import SqsLambdaDynamoDB


def test_sqs_queue_has_dead_letter_queue():
    app = cdk.App()
    stack = SqsLambdaDynamoDB(app, "SqsLambdaDynamoDB")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties(
        "AWS::SQS::Queue",
        {
            "FifoQueue": True,
            "RedrivePolicy": {
                "deadLetterTargetArn": {
                    "Fn::GetAtt": ["QueueDeadLetterQueue16C1D65E", "Arn"]
                },
                "maxReceiveCount": 10,
            },
        },
    )


def test_lambda_function_has_correct_environment_variable():
    app = cdk.App()
    stack = SqsLambdaDynamoDB(app, "SqsLambdaDynamoDB")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties(
        "AWS::Lambda::Function",
        {
            "Environment": {
                "Variables": {
                    "TABLE_NAME": {"Ref": "TableCD117FA1"},
                },
            },
        },
    )


def test_dynamodb_table_has_correct_schema():
    app = cdk.App()
    stack = SqsLambdaDynamoDB(app, "SqsLambdaDynamoDB")
    template = assertions.Template.from_stack(stack)

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


def test_lambda_function_is_subscribed_to_sqs_queue():
    app = cdk.App()
    stack = SqsLambdaDynamoDB(app, "SqsLambdaDynamoDB")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties(
        "AWS::Lambda::EventSourceMapping",
        {
            "EventSourceArn": {"Fn::GetAtt": ["Queue4A7E3555", "Arn"]},
        },
    )
