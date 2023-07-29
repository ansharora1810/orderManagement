import json
import boto3
from botocore.exceptions import ClientError
import re

# def sanitize_topic_name(topic_name):
#     # Remove invalid characters and limit the length to 256 characters
#     return re.sub(r'[^a-zA-Z0-9-_]', '', topic_name)[:256]

def get_topic_arn_from_user_table(user_id):
    dynamodb = boto3.resource('dynamodb')
    user_table = dynamodb.Table('User')

    try:
        response = user_table.scan(
            FilterExpression=boto3.dynamodb.conditions.Key('user_id').eq(user_id),
            ProjectionExpression='topic_arn'
        )
        items = response.get('Items', [])
        if items:
            return items[0].get('topic_arn', None)
        else:
            return None
    except ClientError as e:
        print(f"Error while fetching user data: {e}")
        return None

def handler(event, context):
    print(event)
    # Retrieve the SNS message from the SQS event
    for record in event['Records']:
        sns_message = json.loads(record['body'])
        print(sns_message)
        message_body = json.loads(sns_message['Message'])
        user_id = message_body.get('user_id', '')
        print('user_id', user_id)
        order_details = message_body.get('order_details', [])

        # Get the SNS topic ARN from the User table
        topic_arn = get_topic_arn_from_user_table(user_id)

        if topic_arn:
            # Use Amazon SNS to send the text message
            sns = boto3.client('sns', region_name='us-west-2')  # Replace with the appropriate region
            message = f'Thank you for your order!\n\nOrder Details:\n'
            for item in order_details:
                product_name = item.get('product_name', '')
                quantity = item.get('quantity', 0)
                message += f'{product_name}: {quantity}\n'

            try:
                response = sns.publish(TopicArn=topic_arn, Message=message)
                print(f"Email sent to user with user_id '{user_id}'. Message ID: {response['MessageId']}")
            except ClientError as e:
                print(f"Email not sent to user with user_id '{user_id}'. Error: {e}")
        else:
            print(f"SNS topic ARN not found for user with user_id '{user_id}'.")

    # Prepare the response
    response = {
        "statusCode": 200,
        "body": json.dumps({"message": "Confirmation emails sent successfully!"}),
    }
    return response
