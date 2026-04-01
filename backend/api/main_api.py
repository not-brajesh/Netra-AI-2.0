from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ CORS (frontend connect ke liye)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Home route
@app.get("/")
def home():
    return {
        "message": "NETRA AI Backend Running 🚀"
    }

# ✅ Status API (real-time data)
@app.get("/status")
def status():
    return {
        "people_count": 5,
        "alert": "No threat detected",
        "activity": "Normal movement"
    }

# ✅ Health check
@app.get("/health")
def health():
    return {
        "status": "ok"
    }

# 🔥 NEW: Smart Summary API (GAME CHANGER)
@app.get("/summary")
def summary():
    return {
        "summary": "Currently 5 people are present. No threats detected. Movement is normal and environment is safe."
    }

# 🔥 NEW: Chat API (dynamic response)
@app.get("/chat")
def chat(query: str):
    query = query.lower()

    if "kya ho raha" in query or "what is happening" in query:
        return {
            "response": "5 people are present. No threat detected. Everything is normal."
        }

    elif "kitne log" in query or "people" in query:
        return {
            "response": "Currently 5 people are detected."
        }

    elif "alert" in query:
        return {
            "response": "No alerts right now. System is safe."
        }

    else:
        return {
            "response": "System is running normally. No unusual activity detected."
        }