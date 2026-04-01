import time
import numpy as np


class AbandonedDetector:

    def __init__(self):

        self.objects = {}
        self.abandon_time = 10   # seconds
        self.distance_threshold = 80

    def update(self, tracks):

        abandoned = []

        current_time = time.time()

        for track in tracks:

            track_id = track[4]
            x1, y1, x2, y2 = track[:4]

            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            if track_id not in self.objects:

                self.objects[track_id] = {
                    "pos": (cx, cy),
                    "time": current_time
                }

            else:

                old_pos = self.objects[track_id]["pos"]

                dist = np.linalg.norm(
                    np.array(old_pos) - np.array((cx, cy))
                )

                # object moved
                if dist > self.distance_threshold:

                    self.objects[track_id]["pos"] = (cx, cy)
                    self.objects[track_id]["time"] = current_time

                # object stationary
                else:

                    if current_time - self.objects[track_id]["time"] > self.abandon_time:

                        abandoned.append({
                            "type": "Abandoned Object",
                            "track_id": track_id
                        })

        return abandoned