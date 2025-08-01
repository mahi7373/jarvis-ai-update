import json
from lambda_handler import lambda_handler

# Test the Lambda function locally
def test_lambda():
    # Test GET request
    get_event = {
        'httpMethod': 'GET',
        'body': None
    }
    
    print("Testing GET request...")
    response = lambda_handler(get_event, {})
    print(f"Status: {response['statusCode']}")
    print(f"Response: {json.loads(response['body'])}")
    
    # Test POST request
    post_event = {
        'httpMethod': 'POST',
        'body': json.dumps({
            'query': 'Hello Jarvis, how are you?',
            'brain_mode': 'offline'
        })
    }
    
    print("\nTesting POST request...")
    response = lambda_handler(post_event, {})
    print(f"Status: {response['statusCode']}")
    print(f"Response: {json.loads(response['body'])}")

if __name__ == "__main__":
    test_lambda()