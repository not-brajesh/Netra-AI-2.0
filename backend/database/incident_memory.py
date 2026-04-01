import json
import time
import os

class IncidentMemory:

    def __init__(self):

        self.file = "incidents.json"

        if not os.path.exists(self.file):
            with open(self.file, "w") as f:
                json.dump([], f)


    def store(self, events):

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        with open(self.file, "r") as f:
            data = json.load(f)

        for event in events:

            data.append({
                "time": timestamp,
                "type": event["type"],
                "track_id": event["track_id"]
            })

        with open(self.file, "w") as f:
            json.dump(data, f, indent=2)


    def load(self):

        with open(self.file, "r") as f:
            return json.load(f)
            