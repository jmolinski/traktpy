import json

try:
    with open(".secrets") as f:
        config = json.loads(f.read())
except:
    config = {"client_secret": "", "client_id": ""}
