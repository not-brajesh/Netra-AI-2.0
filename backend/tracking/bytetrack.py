import numpy as np
import supervision as sv
import cv2

from backend.analytics.crowd_analysis import CrowdAnalyzer
from backend.detection.yolo_detector import YOLODetector
from backend.events.abandoned_object import AbandonedDetector
from backend.events.fall_detection import FallDetector


# -----------------------------
# Temporary Face Capture Class
# -----------------------------
class FaceCapture:
    def capture(self, frame, track_id, bbox):
        pass


# Models
detector = YOLODetector()
tracker = sv.ByteTrack()

box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()


# Modules
abandoned = AbandonedDetector()
fall = FallDetector()
crowd = CrowdAnalyzer()
face_capture = FaceCapture()


active_alerts = []


def normalize_event(event):

    if isinstance(event, dict):
        return event

    if isinstance(event, str):
        return {
            "type": event,
            "track_id": -1
        }

    return None


def process_frame(frame):

    global active_alerts

    events = []

    detections = detector.detect(frame)

    if detections is None or len(detections) == 0:
        return frame, events


    detections = np.array(detections)

    xyxy = detections[:, 0:4]
    confidence = detections[:, 4]
    class_id = detections[:, 5].astype(int)


    detections_sv = sv.Detections(
        xyxy=xyxy,
        confidence=confidence,
        class_id=class_id
    )


    tracked = tracker.update_with_detections(detections_sv)


    tracks = []
    labels = []


    for i in range(len(tracked)):

        track_id = tracked.tracker_id[i]

        if track_id is None:
            continue


        x1, y1, x2, y2 = tracked.xyxy[i]
        cls = tracked.class_id[i]


        padding = 15

        x1 = max(0, int(x1 - padding))
        y1 = max(0, int(y1 - padding))
        x2 = int(x2 + padding)
        y2 = int(y2 + padding)


        # Face Capture Disabled Safe Mode
        if cls == 0:
            face_capture.capture(
                frame,
                int(track_id),
                (x1, y1, x2, y2)
            )


        if cls == 0:
            label = f"Person {track_id}"

        elif cls == 24:
            label = f"Bag {track_id}"

        else:
            label = f"Obj {track_id}"


        tracks.append([
            x1,
            y1,
            x2,
            y2,
            int(track_id),
            int(cls)
        ])

        labels.append(label)


    try:
        events.extend(abandoned.update(tracks))
    except Exception as e:
        print("Abandoned Error:", e)


    try:
        events.extend(fall.update(tracks))
    except Exception as e:
        print("Fall Error:", e)


    try:
        events.extend(crowd.analyze(tracks))
    except Exception as e:
        print("Crowd Error:", e)


    normalized_events = []

    for event in events:

        e = normalize_event(event)

        if e:

            normalized_events.append(e)

            if e not in active_alerts:
                active_alerts.append(e)


    frame = box_annotator.annotate(
        scene=frame,
        detections=tracked
    )


    frame = label_annotator.annotate(
        scene=frame,
        detections=tracked,
        labels=labels
    )


    y_offset = 30

    for alert in active_alerts:

        alert_type = alert.get("type", "Unknown")

        if alert_type == "Crowd Analysis":

            text = f"CROWD: {alert.get('level','')} ({alert.get('count','')})"

        else:

            text = f"ALERT: {alert_type} ID {alert.get('track_id','')}"

        cv2.putText(
            frame,
            text,
            (20, y_offset),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )

        y_offset += 30


    return frame, normalized_events