import sys
import os

# -----------------------
# FIX ROOT PATH
# -----------------------

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)


# -----------------------
# IMPORTS
# -----------------------

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse

import cv2
import time
import threading


# -----------------------
# NETRA MODULES
# -----------------------

from backend.tracking.bytetrack import process_frame
from backend.summary.nl_summary import SummaryEngine
from backend.alerts.alert_engine import AlertEngine


# -----------------------
# APP INIT
# -----------------------

app = FastAPI(title="NETRA AI Backend")


# -----------------------
# CORS
# -----------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------
# HOME
# -----------------------

@app.get("/")
def home():
    return {"message": "NETRA AI Backend Running 🚀"}


# -----------------------
# GLOBAL VARIABLES
# -----------------------

camera = cv2.VideoCapture(0)

summary_engine = SummaryEngine()
alert_engine = AlertEngine()

latest_frame = None
latest_alert = "Monitoring..."
summary_result = "Monitoring Started..."

all_events = []


# -----------------------
# SUMMARY THREAD
# -----------------------

def summary_worker():

    global summary_result

    while True:

        try:

            if len(all_events) > 0:

                summary = summary_engine.generate_summary(all_events)

                if summary:
                    summary_result = summary

        except Exception as e:
            print("Summary Error:", e)

        time.sleep(5)


# -----------------------
# FRAME THREAD
# -----------------------

def frame_worker():

    global latest_frame
    global latest_alert
    global all_events

    while True:

        try:

            success, frame = camera.read()

            if not success:
                continue

            frame, events = process_frame(frame)

            if events:
                all_events.extend(events)

            alerts = alert_engine.process(events)

            if alerts:
                latest_alert = str(alerts[-1])

            latest_frame = frame

        except Exception as e:
            print("Frame Error:", e)

        time.sleep(0.03)


# -----------------------
# START THREADS
# -----------------------

threading.Thread(
    target=summary_worker,
    daemon=True
).start()


threading.Thread(
    target=frame_worker,
    daemon=True
).start()


# -----------------------
# VIDEO STREAM
# -----------------------

def generate():

    global latest_frame

    while True:

        if latest_frame is None:
            time.sleep(0.03)
            continue

        ret, buffer = cv2.imencode(".jpg", latest_frame)

        if not ret:
            continue

        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame +
            b'\r\n'
        )

        time.sleep(0.03)


@app.get("/video")
def video():

    return StreamingResponse(
        generate(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )


# -----------------------
# STATUS API
# -----------------------

@app.get("/status")
def status():

    return JSONResponse({
        "people_count": len(all_events),
        "alert": latest_alert,
        "activity": "Running"
    })


# -----------------------
# SUMMARY API
# -----------------------

@app.get("/summary")
def summary():

    return JSONResponse({
        "summary": summary_result
    })


# -----------------------
# HEALTH
# -----------------------

@app.get("/health")
def health():

    return {
        "status": "ok",
        "camera": camera.isOpened()
    }