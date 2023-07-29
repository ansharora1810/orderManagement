import json
import boto3
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


def handler(event, context):
    # Initialize the DynamoDB client
    dynamodb = boto3.resource('dynamodb')

    # Specify the table name
    table_name = 'Products'

    # Get the DynamoDB table
    table = dynamodb.Table(table_name)

    try:
        # Scan the table to fetch all records
        response = table.scan()

        # Extract the items from the response
        items = response['Items']

        # Convert the items to JSON format using the custom DecimalEncoder
        json_data = json.dumps(items, cls=DecimalEncoder)

        # Return the JSON data as the response
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json_data
        }
    except Exception as e:
        # In case of any errors, return an error response
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'error': str(e)})
        }
