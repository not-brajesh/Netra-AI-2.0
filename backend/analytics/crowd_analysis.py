import cv2
import time


class CrowdAnalyzer:

    def __init__(self):

        self.high_threshold = 8
        self.medium_threshold = 4

        self.last_level = "LOW"
        self.last_change_time = time.time()

        self.stability_time = 1.5

    def analyze(self, tracks):

        person_count = 0

        for track in tracks:

            cls = track[5]

            if cls == 0:
                person_count += 1

        if person_count >= self.high_threshold:
            level = "HIGH"

        elif person_count >= self.medium_threshold:
            level = "MEDIUM"

        else:
            level = "LOW"

        current_time = time.time()

        if level != self.last_level:

            if current_time - self.last_change_time > self.stability_time:

                self.last_level = level
                self.last_change_time = current_time

        return [{
            "type": "Crowd Analysis",
            "track_id": -1,
            "count": person_count,
            "level": self.last_level
        }]

    def draw(self, frame, result):

        color = (0, 255, 0)

        if result["level"] == "MEDIUM":
            color = (0, 255, 255)

        if result["level"] == "HIGH":
            color = (0, 0, 255)

        text = f"Crowd: {result['level']} ({result['count']})"

        cv2.putText(
            frame,
            text,
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            color,
            2,
            cv2.LINE_AA
        )

        return frame