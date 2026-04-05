import os
import cv2

class FaceRegistry:

    def __init__(self):

        self.path = "storage/faces"
        os.makedirs(self.path, exist_ok=True)


    def save_face(self, person_id, face):

        file = f"{self.path}/person_{person_id}.jpg"

        if not os.path.exists(file):
            cv2.imwrite(file, face)