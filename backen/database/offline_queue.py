import json
import os

QUEUE_FILE = "offline_visits.json"


def save_offline(data):

    if not os.path.exists(QUEUE_FILE):
        queue = []
    else:
        with open(QUEUE_FILE) as f:
            queue = json.load(f)

    queue.append(data)

    with open(QUEUE_FILE, "w") as f:
        json.dump(queue, f)