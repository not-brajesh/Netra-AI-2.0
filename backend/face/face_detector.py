import cv2

face_model = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

def detect_face(frame):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_model.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5
    )

    return faces