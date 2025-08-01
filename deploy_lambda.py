import boto3
import zipfile
import os

def deploy_to_lambda():
    # Create deployment package
    with zipfile.ZipFile('jarvis-lambda.zip', 'w') as zipf:
        zipf.write('lambda_handler.py')
        zipf.write('brain_manager.py')
        zipf.write('memory.json')
    
    # Deploy to AWS Lambda
    lambda_client = boto3.client('lambda')
    
    with open('jarvis-lambda.zip', 'rb') as zip_file:
        lambda_client.update_function_code(
            FunctionName='jarvis-ai',
            ZipFile=zip_file.read()
        )
    
    print("✅ Deployed to AWS Lambda!")

if __name__ == "__main__":
    deploy_to_lambda()