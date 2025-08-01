# 🚀 AWS Lambda Deployment Instructions

## Prerequisites
1. Install AWS CLI: `pip install awscli`
2. Configure AWS credentials: `aws configure`
3. Set your AWS Access Key, Secret Key, and Region (us-east-1)

## Quick Deploy
```bash
# Install dependencies
pip install boto3

# Run deployment script
python deploy_aws.py
```

## Manual Deployment Steps

### 1. Create Lambda Function
```bash
# Create deployment package
zip -r jarvis-deployment.zip lambda_handler.py brain_manager.py memory.json

# Create Lambda function
aws lambda create-function \
  --function-name JarvisAI-Q \
  --runtime python3.9 \
  --role arn:aws:iam::YOUR_ACCOUNT:role/lambda-execution-role \
  --handler lambda_handler.lambda_handler \
  --zip-file fileb://jarvis-deployment.zip
```

### 2. Create API Gateway
```bash
# Create REST API
aws apigateway create-rest-api --name JarvisAI-API

# Create resource and method (use API Gateway console for easier setup)
```

## Expected Endpoint
After deployment, your endpoint will be:
```
https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod/jarvis
```

## Test Commands
```bash
# Health check
curl https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod/jarvis

# Send query
curl -X POST https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod/jarvis \
  -H "Content-Type: application/json" \
  -d '{"query":"Hello Jarvis","brain_mode":"offline"}'
```