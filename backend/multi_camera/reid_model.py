import numpy as np
import cv2


class PersonReID:

    def __init__(self):
        self.database = {}

    def extract_feature(self, image):

        image = cv2.resize(image, (64,128))
        feature = image.flatten().astype("float32")

        norm = np.linalg.norm(feature)

        if norm == 0:
            return feature

        feature = feature / norm

        return feature


    def register(self, person_id, image):

        feature = self.extract_feature(image)

        self.database[person_id] = feature


    def match(self, image):

        if len(self.database) == 0:
            return None

        feature = self.extract_feature(image)

        best_id = None
        best_score = 0

        for pid, stored in self.database.items():

            score = np.dot(feature, stored)

            if score > best_score:
                best_score = score
                best_id = pid

        if best_score > 0.85:
            return best_id

        return None