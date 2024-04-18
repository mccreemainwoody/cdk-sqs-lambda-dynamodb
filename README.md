
# CDK SQS Lambda DynamoDB

This repository is a teeny-tiny project I've made to train with AWS services.

This basically uses the AWS Cloud Development Kit (CDK) to create a stack 
composed of mainly 3 things :
- A SQS FIFO queue with a dead-letter queue.
- A Lambda function, with the main SQS queue as its event source.
- A DynamoDB table.

When triggered, the Lambda function reads the SQS message, and writes it to the
DynamoDB table.

This CDK project is made using Python 3.12 with Poetry as the package manager.
It has also been first created based on the sample-app template, so there are
still some remanents of the original project in some places here are there.

And that's it ! If you also happen to learn how things work with AWS, feel free
to use this project and give a look at how it's made.


## Usage (you can get the same explanation on your personal projects by setting up a CDK sample-app template project.)
You should explore the contents of this project. It demonstrates a CDK app with an instance of a stack (`src_stack`)
which contains an Amazon SQS queue that is subscribed to an Amazon SNS topic.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization process also creates
a virtualenv within this project, stored under the .venv directory.  To create the virtualenv
it assumes that there is a `python3` executable in your path with access to the `venv` package.
If for any reason the automatic creation of the virtualenv fails, you can create the virtualenv
manually once the init process completes.

To manually create a virtualenv on MacOS and Linux:

```
$ python -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

You can now begin exploring the source code, contained in the hello directory.
There is also a very trivial test included that can be run like this:

```
$ pytest
```

To add additional dependencies, for example other CDK libraries, just add to
your requirements.txt file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
