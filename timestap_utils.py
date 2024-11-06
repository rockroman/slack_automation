import json
from datetime import datetime
import time


TIMESTAMP_FILE = 'last_timestamp.json'

def save_timestamp(timestamp):
    with open(TIMESTAMP_FILE, 'w') as f:
        json.dump({'timestamp': timestamp}, f)


def load_timestamp():
    try:
        with open(TIMESTAMP_FILE, 'r') as f:
            data = json.load(f)
            return float(data['timestamp'])
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return datetime.now().timestamp()



def format_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M:%S')