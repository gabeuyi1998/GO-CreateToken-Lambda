import json
import boto3

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TokenStore')

# Initialize SNS client
sns = boto3.client('sns')

def lambda_handler(event, context):
    # Retrieve the token ID from the query parameters
    token_id = event['queryStringParameters']['token_id']
    
    # Retrieve the token from DynamoDB
    response = table.get_item(
        Key={
            'TokenID': token_id
        }
    )
    
    if 'Item' in response:
        # Publish a message to SNS
        sns.publish(
            TopicArn='arn:aws:sns:ap-southeast-2:866934333672:GoTokenNotificationTopic',
            Message=f'Token {token_id} has been retrieved from DynamoDB',
            Subject='Token Retrieved'
        )
        return {
            'statusCode': 200,
            'body': json.dumps(response['Item'], default=str)
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Token not found'})
        }
