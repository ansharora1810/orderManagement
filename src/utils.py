import json


def get_json_payload(evt, k='body'):
    body = evt.get(k)
    return json.loads(body)
