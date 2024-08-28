import json
import boto3
import random
import string

# Initialize DynamoDB resource and Lambda client
dynamodb = boto3.resource('dynamodb')
lambda_client = boto3.client('lambda')
table = dynamodb.Table('TokenStore')

def generate_token(length=6):
    """Generates a random token with the specified length."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def lambda_handler(event, context):
    try:
        # Generate a unique 6-character token
        token_id = generate_token()
        
        # Store the token in DynamoDB
        table.put_item(
            Item={
                'TokenID': token_id,
                'Valid': True
            }
        )
        
        # Invoke the RetrieveToken Lambda function asynchronously
        response = lambda_client.invoke(
            FunctionName='RetrieveTokenFunction',  
            InvocationType='Event',  # Asynchronous invocation
            Payload=json.dumps({'queryStringParameters': {'token_id': token_id}})
        )
        
        if response['StatusCode'] != 202:
            return {
                'statusCode': 500,
                'body': json.dumps({'Message': 'Error invoking the RetrieveTokenFunction'})
            }
        
        # Return the token in the response
        return {
            'statusCode': 200,
            'body': json.dumps({'TokenID': token_id, 'Message': 'Token created and retrieval initiated'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'Message': f'Internal server error: {str(e)}'})
        }