import time
import ollama
import json
import os


class SummaryEngine:

    def __init__(self):

        self.story_events = []
        self.last_summary_time = time.time()
        self.summary_interval = 10   # reduced for testing

        self.memory_file = "incident_memory.json"

        if not os.path.exists(self.memory_file):
            with open(self.memory_file, "w") as f:
                json.dump([], f)


    def save_incident(self, events):

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        with open(self.memory_file, "r") as f:
            data = json.load(f)

        for event in events:

            data.append({
                "time": timestamp,
                "event": event["type"],
                "person_id": event["track_id"]
            })

        with open(self.memory_file, "w") as f:
            json.dump(data, f, indent=2)


    def generate_summary(self, events):

        if len(events) == 0:
            return ""

        timestamp = time.strftime("%H:%M:%S")

        # Save incident
        self.save_incident(events)

        # Store story
        for event in events:

            text = f"{timestamp} - {event['type']} by Person ID {event['track_id']}"
            self.story_events.append(text)


        # ALWAYS generate summary if called at end
        if time.time() - self.last_summary_time < self.summary_interval and len(self.story_events) < 3:
            return ""

        self.last_summary_time = time.time()

        prompt = f"""
You are NETRA-AI intelligent surveillance system.

Convert logs into incident report.

Events:

{self.story_events}

Write:

1 Timeline
2 What happened
3 Suspicious behaviour
4 Final summary

Professional CCTV tone
"""

        try:

            response = ollama.chat(
                model="qwen2.5",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            self.story_events = []

            return response["message"]["content"]

        except Exception as e:

            return f"Summary Error: {str(e)}"