from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.models import Model

from model.constants import DynamoDBConstants


class DDBProduct(Model):

    class Meta:
        table_name = DynamoDBConstants.PRODUCT_TABLE
        region = DynamoDBConstants.REGION

    request_id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    brand = UnicodeAttribute()
    quantity = NumberAttribute()
