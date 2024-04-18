import boto3
import os


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    for record in event["Records"]:
        document = {
            "id": record["messageId"],
            "message": record["body"],
            "timestamp": record["attributes"]["SentTimestamp"]
        }

        table.put_item(Item=document)

    return {"statusCode": 200, "body": "Records inserted successfully"}
