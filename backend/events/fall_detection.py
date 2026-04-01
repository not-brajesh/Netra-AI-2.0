import time


class FallDetector:

    def __init__(self):

        self.fall_ratio = 1.3
        self.fall_memory = {}
        self.fall_delay = 2

    def update(self, tracks):

        events = []

        current_time = time.time()

        for track in tracks:

            # FIX HERE (6 values)
            x1, y1, x2, y2, track_id, _ = track

            width = x2 - x1
            height = y2 - y1

            if height == 0:
                continue

            ratio = width / height

            if ratio > self.fall_ratio:

                if track_id not in self.fall_memory:
                    self.fall_memory[track_id] = current_time

                else:

                    if current_time - self.fall_memory[track_id] > self.fall_delay:

                        events.append({
                            "type": "Fall Detected",
                            "track_id": track_id
                        })

            else:

                if track_id in self.fall_memory:
                    del self.fall_memory[track_id]

        return events