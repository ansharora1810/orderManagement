import json
import boto3
import uuid
import re

def sanitize_topic_name(topic_name):
    # Remove invalid characters and limit the length to 256 characters
    return re.sub(r'[^a-zA-Z0-9-_]', '', topic_name)[:256]

def subscribe_email_to_topic(topic_arn, email):
    sns = boto3.client('sns', region_name='us-west-2')  # Replace with the appropriate region
    try:
        response = sns.subscribe(
            TopicArn=topic_arn,
            Protocol='email',
            Endpoint=email
        )
        return True
    except ClientError as e:
        print(f"Failed to subscribe email to topic. Error: {e}")
        return False

def handler(event, context):
    print(event)
    # Retrieve the user place_order data from the API event
    user_data = json.loads(event.get('body'))

    name = user_data.get('name', '')
    email = user_data.get('email', '')
    phone = user_data.get('phone', '')

    # Generate a user_id for the new user
    user_id = str(uuid.uuid4())

    # Store the user details in DynamoDB User table
    dynamodb = boto3.resource('dynamodb')
    user_table = dynamodb.Table('User')

    topic_name = f'Order_{user_id}'  # Use a unique topic name
    sanitized_topic_name = sanitize_topic_name(topic_name)

    # Create an SNS topic
    sns = boto3.client('sns', region_name='us-west-2')  # Replace with the appropriate region
    try:
        response = sns.create_topic(Name=sanitized_topic_name)
        topic_arn = response['TopicArn']

        # Subscribe the email address to the topic
        if subscribe_email_to_topic(topic_arn, email):
            user_item = {
                'user_id': user_id,
                'name': name,
                'email': email,
                'phone': phone,
                'topic_arn': topic_arn
            }

            user_table.put_item(Item=user_item)
        else:
            print(f"Failed to subscribe email '{email}' to the topic.")
    except ClientError as e:
        print(f"Failed to create topic or subscribe email to topic. Error: {e}")

    # Prepare the response
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        },
        "body": json.dumps({"message": "User registered successfully!", "user_id": user_id}),
    }

    return response
