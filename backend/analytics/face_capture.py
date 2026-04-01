import cv2
import os
import time
import numpy as np


class FaceCapture:

    def __init__(self):

        self.face_detector = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        self.saved_ids = {}

        self.save_path = "backend/storage/persons"

        os.makedirs(self.save_path, exist_ok=True)


    def capture(self, frame, track_id, bbox):

        if track_id in self.saved_ids:
            return None

        x1, y1, x2, y2 = bbox

        person_crop = frame[y1:y2, x1:x2]

        if person_crop.size == 0:
            return None

        gray = cv2.cvtColor(person_crop, cv2.COLOR_BGR2GRAY)

        faces = self.face_detector.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(30, 30)
        )

        if len(faces) == 0:
            return None

        # Take biggest face
        face = max(faces, key=lambda f: f[2]*f[3])

        fx, fy, fw, fh = face

        face_img = person_crop[fy:fy+fh, fx:fx+fw]

        filename = f"person_{track_id}.jpg"

        filepath = os.path.join(self.save_path, filename)

        cv2.imwrite(filepath, face_img)

        self.saved_ids[track_id] = filepath

        return filepath