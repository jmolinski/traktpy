import json

try:
    with open(".secrets") as f:
        config = json.loads(f.read())
except:  # NOQA
    config = {"client_secret": "", "client_id": ""}
