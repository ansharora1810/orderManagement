from enum import Enum


class DynamoDBConstants(Enum, str):
    PRODUCT_TABLE = "products"
    REGION = "us-east-1"
    USER_TABLE = "users"

