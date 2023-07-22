from typing import Dict, Any

from model.user import User
from src.utils import get_json_payload
from storage.user import DDBUser


def validate_params(body: Dict[str, Any]):
    expected_keys = ['name', 'email', 'phone']
    if not all(key in body for key in expected_keys):
        raise ValueError("Missing input parameters!")


def handler(event, _):
    request_body = get_json_payload(event)
    validate_params(request_body)
    user = User.model_validate(request_body)
    ddb_user = DDBUser.from_user(user)
    user_id = ddb_user.user_id
    ddb_user.save()
    return {
        "user_id": user_id
    }