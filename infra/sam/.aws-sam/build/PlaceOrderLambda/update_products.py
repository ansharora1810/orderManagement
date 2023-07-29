import json
import boto3


def handler(event, context):
    print(event)
    # Retrieve the order details from the SQS event
    for record in event['Records']:
        message_body = json.loads(record['body'])
        print('message_body', message_body)

        # Parse the nested JSON inside the 'Message' key
        sns_message = json.loads(message_body['Message'])
        user_id = sns_message.get('user_id', '')
        print('user_id', user_id)
        order_details = sns_message.get('order_details', [])
        print('order_details', order_details)

        # Update the Products table in DynamoDB
        dynamodb = boto3.resource('dynamodb')
        products_table = dynamodb.Table('Products')

        for item in order_details:
            product_name = item.get('product_name', '')
            quantity = item.get('quantity', 0)

            # Reduce the quantity of the ordered product in the Products table
            response = products_table.update_item(
                Key={'product_name': product_name},
                UpdateExpression='SET quantity = quantity - :val',
                ExpressionAttributeValues={':val': quantity},
                ReturnValues='ALL_NEW'  # Optional: Return the updated item attributes
            )

            updated_item = response.get('Attributes', None)

            # Optionally, you can handle the case where the product doesn't exist in the table
            if not updated_item:
                print(f"Product '{product_name}' not found in the Products table.")
                # You can choose to log, raise an exception, or take appropriate action here.

    # Prepare the response
    response = {
        "statusCode": 200,
        "body": json.dumps({"message": "Products updated successfully!"}),
    }

    return response
