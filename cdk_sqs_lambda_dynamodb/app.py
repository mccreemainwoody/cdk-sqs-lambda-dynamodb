#!/usr/bin/env python3

import aws_cdk as cdk

from stacks import SqsLambdaDynamoDB


def main() -> None:
    app = cdk.App()

    SqsLambdaDynamoDB(app, "SqsLambdaDynamoDB")

    app.synth()


if __name__ == "__main__":
    main()
