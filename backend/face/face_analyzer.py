import cv2
import numpy as np

def is_clear_face(face):

    gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

    blur = cv2.Laplacian(gray, cv2.CV_64F).var()

    if blur > 100:
        return True

    return False


def is_masked(face):

    h, w, _ = face.shape

    lower = face[int(h*0.5):h, 0:w]

    brightness = lower.mean()

    if brightness < 70:
        return True

    return False