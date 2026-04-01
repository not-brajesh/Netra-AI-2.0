import cv2
import torch
from ultralytics import YOLO


class YOLODetector:

    def __init__(self):

        self.device = "mps" if torch.backends.mps.is_available() else "cpu"

        # Ultra fast model
        self.fast_model = YOLO("yolov8n.pt")
        self.fast_model.to(self.device)

        # Accurate model
        self.slow_model = YOLO("yolov8s.pt")
        self.slow_model.to(self.device)

        self.frame_count = 0


    def detect(self, frame):

        self.frame_count += 1
        detections = []

        # FAST MODEL (Every frame)
        results = self.fast_model(
            frame,
            conf=0.35,
            verbose=False,
            device=self.device
        )

        for r in results:

            if r.boxes is None:
                continue

            for box in r.boxes:

                cls = int(box.cls[0])

                # Only person fast detection
                if cls != 0:
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])

                detections.append([x1, y1, x2, y2, conf, cls])


        # SLOW MODEL (Every 20 frame)
        if self.frame_count % 20 == 0:

            results = self.slow_model(
                frame,
                conf=0.45,
                verbose=False,
                device=self.device
            )

            for r in results:

                if r.boxes is None:
                    continue

                for box in r.boxes:

                    cls = int(box.cls[0])

                    # Bags only
                    if cls not in [24, 26]:
                        continue

                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = float(box.conf[0])

                    detections.append([x1, y1, x2, y2, conf, cls])


        return detections