import boto3
import zipfile
import json
import time
import os

def create_lambda_package():
    # Create deployment package
    with zipfile.ZipFile('jarvis-deployment.zip', 'w') as zipf:
        zipf.write('lambda_handler.py')
        zipf.write('brain_manager.py')
        
        # Create empty memory.json if it doesn't exist
        if not os.path.exists('memory.json'):
            with open('memory.json', 'w') as f:
                json.dump({"conversations": [], "preferences": {}}, f)
        zipf.write('memory.json')
    
    print("Lambda package created")

def deploy_to_aws():
    # AWS clients
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    apigateway_client = boto3.client('apigateway', region_name='us-east-1')
    iam_client = boto3.client('iam')
    
    # Create IAM role for Lambda
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "lambda.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }
        ]
    }
    
    try:
        role_response = iam_client.create_role(
            RoleName='JarvisAI-Lambda-Role',
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description='Role for Jarvis AI Lambda function'
        )
        role_arn = role_response['Role']['Arn']
        print("IAM role created")
        
        # Attach basic execution policy
        iam_client.attach_role_policy(
            RoleName='JarvisAI-Lambda-Role',
            PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
        )
        
        # Wait for role to be available
        time.sleep(10)
        
    except iam_client.exceptions.EntityAlreadyExistsException:
        role_arn = f"arn:aws:iam::{boto3.client('sts').get_caller_identity()['Account']}:role/JarvisAI-Lambda-Role"
        print("Using existing IAM role")
    
    # Create Lambda function
    try:
        with open('jarvis-deployment.zip', 'rb') as zip_file:
            lambda_response = lambda_client.create_function(
                FunctionName='JarvisAI-Q',
                Runtime='python3.9',
                Role=role_arn,
                Handler='lambda_handler.lambda_handler',
                Code={'ZipFile': zip_file.read()},
                Description='Jarvis AI Assistant with Dual Brain',
                Timeout=30,
                MemorySize=512
            )
        print("Lambda function created")
        
    except lambda_client.exceptions.ResourceConflictException:
        # Update existing function
        with open('jarvis-deployment.zip', 'rb') as zip_file:
            lambda_client.update_function_code(
                FunctionName='JarvisAI-Q',
                ZipFile=zip_file.read()
            )
        print("Lambda function updated")
    
    # Create API Gateway
    try:
        api_response = apigateway_client.create_rest_api(
            name='JarvisAI-API',
            description='API for Jarvis AI Assistant'
        )
        api_id = api_response['id']
        print("API Gateway created")
        
    except Exception as e:
        # Get existing API
        apis = apigateway_client.get_rest_apis()
        api_id = None
        for api in apis['items']:
            if api['name'] == 'JarvisAI-API':
                api_id = api['id']
                break
        
        if not api_id:
            raise e
        print("Using existing API Gateway")
    
    # Get root resource
    resources = apigateway_client.get_resources(restApiId=api_id)
    root_id = None
    for resource in resources['items']:
        if resource['path'] == '/':
            root_id = resource['id']
            break
    
    # Create /jarvis resource
    try:
        resource_response = apigateway_client.create_resource(
            restApiId=api_id,
            parentId=root_id,
            pathPart='jarvis'
        )
        resource_id = resource_response['id']
        print("API resource created")
        
    except Exception:
        # Get existing resource
        for resource in resources['items']:
            if resource['path'] == '/jarvis':
                resource_id = resource['id']
                break
        print("Using existing API resource")
    
    # Create POST method
    try:
        apigateway_client.put_method(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod='POST',
            authorizationType='NONE'
        )
        
        # Set up Lambda integration
        account_id = boto3.client('sts').get_caller_identity()['Account']
        lambda_uri = f"arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:{account_id}:function:JarvisAI-Q/invocations"
        
        apigateway_client.put_integration(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod='POST',
            type='AWS_PROXY',
            integrationHttpMethod='POST',
            uri=lambda_uri
        )
        
        # Add Lambda permission
        lambda_client.add_permission(
            FunctionName='JarvisAI-Q',
            StatementId='api-gateway-invoke',
            Action='lambda:InvokeFunction',
            Principal='apigateway.amazonaws.com',
            SourceArn=f"arn:aws:execute-api:us-east-1:{account_id}:{api_id}/*/*"
        )
        
        print("API method configured")
        
    except Exception as e:
        print(f"Method might already exist: {e}")
    
    # Deploy API
    try:
        apigateway_client.create_deployment(
            restApiId=api_id,
            stageName='prod'
        )
        print("API deployed")
        
    except Exception:
        print("API deployment updated")
    
    # Return endpoint URL
    endpoint_url = f"https://{api_id}.execute-api.us-east-1.amazonaws.com/prod/jarvis"
    return endpoint_url

if __name__ == "__main__":
    print("Deploying Jarvis AI to AWS Lambda...")
    
    create_lambda_package()
    endpoint_url = deploy_to_aws()
    
    print(f"\nDeployment Complete!")
    print(f"Endpoint URL: {endpoint_url}")
    print(f"\nTest Commands:")
    print(f"GET:  curl {endpoint_url}")
    print(f"POST: curl -X POST {endpoint_url} -H 'Content-Type: application/json' -d '{{\"query\":\"Hello Jarvis\",\"brain_mode\":\"offline\"}}'")
    
    # Cleanup
    os.remove('jarvis-deployment.zip')