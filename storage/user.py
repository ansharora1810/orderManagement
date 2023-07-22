import uuid

from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.models import Model

from model.constants import DynamoDBConstants
from model.user import User


class DDBUser(Model):
    class Meta:
        table_name = DynamoDBConstants.USER_TABLE
        region = DynamoDBConstants.REGION

    user_id = UnicodeAttribute(hash_key=True, default=str(uuid.uuid4))
    name = UnicodeAttribute()
    email = UnicodeAttribute()
    phone = NumberAttribute()

    @classmethod
    def from_user(cls, user: User) -> "DDBUser":
        return cls(
            name=user.name,
            email=user.email,
            phone=user.phone
        )
