import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import cv2
import time
import threading

from backend.alerts.alert_engine import AlertEngine
from backend.tracking.bytetrack import process_frame
from backend.summary.nl_summary import SummaryEngine


summary_engine = SummaryEngine()
alert_engine = AlertEngine()

cap = cv2.VideoCapture(0)

print("NETRA-AI Started...")
print("Press Q to exit")

all_events = []
summary_result = ""


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


# Start Thread
thread = threading.Thread(target=summary_worker, daemon=True)
thread.start()


while True:

    ret, frame = cap.read()

    if not ret:
        print("Camera not detected")
        break


    # Detection Pipeline
    frame, events = process_frame(frame)

    if events:
        all_events.extend(events)


    # ALERT ENGINE

    alerts = alert_engine.process(events)

    for alert in alerts:
        print("🚨 ALERT:", alert)


    # Show frame
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

print("="*60)


cap.release()
cv2.destroyAllWindows()