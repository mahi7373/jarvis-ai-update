import json
from brain_manager import BrainManager

# Initialize Jarvis for Lambda
jarvis_brain = BrainManager()

def lambda_handler(event, context):
    try:
        # Parse input
        body = json.loads(event.get('body', '{}'))
        query = body.get('query', '')
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
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'response': response,
                'brain_mode': jarvis_brain.current_brain,
                'timestamp': jarvis_brain.memory['conversations'][-1]['timestamp']
            })
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }