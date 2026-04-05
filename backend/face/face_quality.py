import cv2
import numpy as np

def is_clear_face(face):

    gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

    blur = cv2.Laplacian(gray, cv2.CV_64F).var()

    if blur > 80:
        return True

    return False