import cv2
import sys
import os
import threading

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from backend.tracking.bytetrack import process_frame


camera_sources = [0, 1]

frames = [None] * len(camera_sources)
caps = []


def camera_thread(index, source):

    cap = cv2.VideoCapture(source)

    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    caps.append(cap)

    while True:

        ret, frame = cap.read()

        if ret:
            frames[index] = frame


# Start Threads
for i, src in enumerate(camera_sources):

    thread = threading.Thread(
        target=camera_thread,
        args=(i, src),
        daemon=True
    )

    thread.start()


while True:

    valid_frames = []

    for f in frames:

        if f is not None:
            valid_frames.append(cv2.resize(f, (640,480)))


    if len(valid_frames) == 0:
        continue


    # Merge frames
    if len(valid_frames) == 1:

        merged = valid_frames[0]

    else:

        merged = cv2.hconcat(valid_frames)


    # Single detection (smooth)
    output = process_frame(merged)


    cv2.imshow("NETRA-AI Multi Camera", output)


    if cv2.waitKey(1) & 0xFF == 27:
        break


for cap in caps:
    cap.release()

cv2.destroyAllWindows()