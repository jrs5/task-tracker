# CDK Python project for Task Tracker API

This is a simple project to deploy FastAPI with CDK. All the CDK dependencies are part of the overall project and are managed with Poetry. Make sure to bootstrap the project before using `cdk` commands. To add additional dependencies, for example other CDK libraries, just add them to the `pyproject.toml` file and rerun the `make install-dev` command.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

## Useful commands

- `cdk ls` list all stacks in the app
- `cdk synth` emits the synthesized CloudFormation template
- `cdk deploy` deploy this stack to your default AWS account/region
- `cdk diff` compare deployed stack with current state
- `cdk docs` open CDK documentation
