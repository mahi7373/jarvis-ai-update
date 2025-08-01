import json
from brain_manager import BrainManager

# Initialize Jarvis for Lambda
jarvis_brain = BrainManager()

def lambda_handler(event, context):
    try:
        # Handle both GET and POST requests
        if event.get('httpMethod') == 'GET':
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'message': 'Jarvis AI is running!',
                    'brain_mode': jarvis_brain.current_brain,
                    'endpoints': {
                        'POST /jarvis': 'Send query to Jarvis',
                        'GET /jarvis': 'Health check'
                    }
                })
            }
        
        # Parse POST request
        body = event.get('body', '{}')
        if isinstance(body, str):
            body = json.loads(body)
        
        query = body.get('query', 'Hello Jarvis')
        brain_mode = body.get('brain_mode', 'offline')
        
        # Switch brain mode if requested
        if brain_mode == 'online':
            jarvis_brain.switch_to_online()
        else:
            jarvis_brain.switch_to_offline()
        
        # Process query
        response = jarvis_brain.think(query)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({
                'query': query,
                'response': response,
                'brain_mode': jarvis_brain.current_brain,
                'timestamp': jarvis_brain.memory['conversations'][-1]['timestamp'] if jarvis_brain.memory['conversations'] else None
            })
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e),
                'message': 'Jarvis AI encountered an error'
            })
        }