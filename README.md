## Installation and Deployment

### Installing Serverless Plugins
To install the necessary serverless plugins, run the following command:
```bash
serverless plugin install -n serverless-python-requirements
serverless plugin install -n serverless-offline
```

### AWS Credentials Configuration
Configure your AWS credentials by editing the `~/.aws/credentials` file. You can use `vi` or your preferred text editor:
```bash
vi ~/.aws/credentials
```

### Deploying to AWS
To deploy the application to AWS with the `dev` stage, use the following command:
```bash
serverless deploy --stage dev
```

### Running Locally
To run the application locally with the `dev` stage, use the following command:
```bash
serverless offline --stage dev
```