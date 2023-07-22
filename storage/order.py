from pynamodb.attributes import UnicodeAttribute, NumberAttribute, ListAttribute
from pynamodb.models import Model

from model.constants import DynamoDBConstants
from model.order_item import OrderItem


class DDBOrder(Model):

    class Meta:
        table_name = DynamoDBConstants.USER_TABLE
        region = DynamoDBConstants.REGION

    request_id = UnicodeAttribute(hash_key=True)
    order_items = ListAttribute(of=OrderItem)
    user_id = UnicodeAttribute()
    total_value = NumberAttribute()
    status = NumberAttribute()

