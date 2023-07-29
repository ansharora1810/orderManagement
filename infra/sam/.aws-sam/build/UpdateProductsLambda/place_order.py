import json
import boto3
import uuid


def handler(event, context):
    print(event)
    # Retrieve the order details from the API event
    order_details = json.loads(event.get('body'))

    # Generate an order_id for the new order
    order_id = str(uuid.uuid4())

    # Add the order_id to the order details
    order_details['order_id'] = order_id

    # Publish the order details to the "OrderConfirmationTopic" SNS topic
    sns = boto3.client('sns')
    topic_arn = 'arn:aws:sns:us-west-2:121724640456:Orders'  # Replace REGION and ACCOUNT_ID
    sns.publish(
        TopicArn=topic_arn,
        Message=json.dumps(order_details)
    )

    # Store the order details in the "Orders" DynamoDB table
    dynamodb = boto3.resource('dynamodb')
    orders_table = dynamodb.Table('Orders')
    orders_table.put_item(Item=order_details)

    # Prepare the response
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        },
        "body": json.dumps({"message": "Order placed successfully!", "order_details": order_details}),
    }

    return response
