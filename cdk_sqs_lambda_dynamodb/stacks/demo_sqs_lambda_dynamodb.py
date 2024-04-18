from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_sqs as sqs,
    aws_dynamodb as dynamodb,
    aws_lambda_event_sources as lambda_event_sources,
)
from constructs import Construct
from pathlib import Path


class SqsLambdaDynamoDB(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Add a CloudFormation template comment
        self.template_options.description = (
            "A small AWS CDK project that allows to write messages to a "
            "DynamoDB database from an SQS queue. "
            "It's pretty, it's all fresh and new and it works :D"
        )

        # Create a DynamoDB table
        table = dynamodb.Table(
            self, "Table",
            table_name="sqs-lambda-dynamodb",
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="timestamp",
                type=dynamodb.AttributeType.STRING
            ),
            write_capacity=5,
            read_capacity=3,
        )

        # Create a Lambda function
        function = _lambda.Function(
            self, "Function",
            function_name="sqs-lambda-dynamodb",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="lambda_function.lambda_handler",
            code=_lambda.Code.from_asset(
                str(Path(__file__).parent.parent / "compute" / "sqs_to_dynamodb")
            ),
            environment={
                "TABLE_NAME": table.table_name
            }
        )

        # Create an SQS queue
        dead_letter_queue = sqs.Queue(
            self,  "QueueDeadLetterQueue",
            queue_name="sqs-lambda-dynamodb-dead-letter-queue.fifo",
            fifo=True
        )

        queue = sqs.Queue(
            self, "Queue",
            queue_name="sqs-lambda-dynamodb.fifo",
            fifo=True,
            dead_letter_queue=sqs.DeadLetterQueue(
                max_receive_count=10,
                queue=dead_letter_queue
            )
        )

        # Grant the Lambda function permissions to write to the DynamoDB table
        table.grant_write_data(function)

        # Grant the Lambda function permissions to read from the SQS queue
        # and the dead letter queue
        queue.grant_consume_messages(function)

        dead_letter_queue.grant_send_messages(function)

        # Set the SQS Queue as an event source for the Lambda function
        function_event_source = lambda_event_sources.SqsEventSource(queue)

        function.add_event_source(function_event_source)
