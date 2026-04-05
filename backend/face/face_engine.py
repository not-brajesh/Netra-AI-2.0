import insightface
import cv2
import numpy as np

class FaceEngine:

    def __init__(self):

        self.app = insightface.app.FaceAnalysis()
        self.app.prepare(ctx_id=0)

    def detect(self, frame):

        faces = self.app.get(frame)

        return faces