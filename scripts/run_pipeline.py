import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import cv2
import time
import threading

from backend.alerts.alert_engine import AlertEngine
from backend.tracking.bytetrack import process_frame
from backend.summary.nl_summary import SummaryEngine
from backend.database.person_registry import PersonRegistry
from backend.multi_camera.reid_model import PersonReID

# FACE ENGINE
from backend.face.face_engine import FaceEngine
from backend.face.face_analyzer import is_clear_face, is_masked
from backend.face.face_registry import FaceRegistry


summary_engine = SummaryEngine()
alert_engine = AlertEngine()
person_registry = PersonRegistry()
reid_engine = PersonReID()
face_registry = FaceRegistry()
face_engine = FaceEngine()

cap = cv2.VideoCapture(0)

print("NETRA-AI Started...")
print("Press Q to exit")

all_events = []
summary_result = ""

masked_faces = []
unclear_faces = []


# -------------------------
# Background Summary Thread
# -------------------------

def summary_worker():

    global summary_result

    while True:

        if len(all_events) > 0:

            summary = summary_engine.generate_summary(all_events)

            if summary:
                summary_result = summary

        time.sleep(5)


thread = threading.Thread(target=summary_worker, daemon=True)
thread.start()


while True:

    ret, frame = cap.read()

    if not ret:
        print("Camera not detected")
        break


    # -------------------------
    # Detection Pipeline
    # -------------------------

    frame, events = process_frame(frame)


    # -------------------------
    # FACE DETECTION
    # -------------------------

    faces = face_engine.detect(frame)


    # -------------------------
    # PERSON PROCESSING
    # -------------------------

    for event in events:

        if "id" in event and "bbox" in event:

            person_id = event["id"]
            bbox = event["bbox"]

            x1, y1, x2, y2 = map(int, bbox)

            person_crop = frame[y1:y2, x1:x2]


            # -------------------------
            # RE-ID
            # -------------------------

            matched_id = reid_engine.match(person_crop)

            if matched_id is not None:
                person_id = matched_id

            else:
                reid_engine.register(person_id, person_crop)


            # -------------------------
            # SAVE PERSON IMAGE
            # -------------------------

            person_registry.save_person(
                person_id,
                frame,
                bbox
            )


            # -------------------------
            # FACE MATCH
            # -------------------------

            for face in faces:

                fx1, fy1, fx2, fy2 = face.bbox.astype(int)

                face_img = frame[fy1:fy2, fx1:fx2]

                # check face inside bbox

                if fx1 > x1 and fy1 > y1 and fx2 < x2 and fy2 < y2:

                    if is_masked(face_img):

                        masked_faces.append(person_id)

                    elif not is_clear_face(face_img):

                        unclear_faces.append(person_id)

                    else:

                        face_registry.save_face(
                            person_id,
                            face_img
                        )

                        print(f"Face saved for person {person_id}")


            # -------------------------
            # DRAW BOX
            # -------------------------

            name = person_registry.get_person_name(person_id)

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0,255,0),
                2
            )


            cv2.putText(
                frame,
                f"{name} (ID {person_id})",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0,255,0),
                2
            )


    if events:
        all_events.extend(events)


    # -------------------------
    # ALERT ENGINE
    # -------------------------

    alerts = alert_engine.process(events)

    for alert in alerts:
        print("🚨 ALERT:", alert)


    # -------------------------
    # SHOW FRAME
    # -------------------------

    cv2.imshow("NETRA AI LIVE", frame)


    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break


# -------------------------
# FINAL REPORT
# -------------------------

print("\n")
print("="*60)
print("FINAL INCIDENT REPORT")
print("="*60)

if summary_result:
    print(summary_result)

else:

    final_summary = summary_engine.generate_summary(all_events)

    if final_summary:
        print(final_summary)

    else:
        print("No incidents recorded")


# -------------------------
# MASK REPORT
# -------------------------

print("\n")
print("="*60)
print("MASKED FACE REPORT")
print("="*60)

if masked_faces:

    for pid in set(masked_faces):
        print(f"Person {pid} masked face")

else:

    print("No masked faces")


# -------------------------
# UNCLEAR REPORT
# -------------------------

print("\n")
print("="*60)
print("UNCLEAR FACE REPORT")
print("="*60)

if unclear_faces:

    for pid in set(unclear_faces):
        print(f"Person {pid} unclear face")

else:

    print("All faces clear")

print("="*60)


cap.release()
cv2.destroyAllWindows()