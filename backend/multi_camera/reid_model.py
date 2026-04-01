import cv2
import numpy as np


def extract_feature(frame, bbox):

    x1,y1,x2,y2 = bbox

    person = frame[y1:y2, x1:x2]

    if person.size == 0:
        return None

    person = cv2.resize(person,(64,128))

    # Color histogram
    hist = cv2.calcHist(
        [person],
        [0,1,2],
        None,
        [8,8,8],
        [0,256,0,256,0,256]
    )

    cv2.normalize(hist, hist)

    # shape feature
    h,w,_ = person.shape
    shape = np.array([h/w])

    feature = np.concatenate([
        hist.flatten(),
        shape
    ])

    return feature


def compare_features(f1, f2):

    if f1 is None or f2 is None:
        return 0

    hist_score = cv2.compareHist(
        f1[:-1].astype("float32"),
        f2[:-1].astype("float32"),
        cv2.HISTCMP_CORREL
    )

    shape_score = 1 - abs(f1[-1] - f2[-1])

    final_score = 0.8 * hist_score + 0.2 * shape_score

    return final_score