from datetime import datetime
from zoneinfo import ZoneInfo
import firebase_admin
from firebase_admin import credentials, firestore

# set up logging
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def log_event(message, level="INFO"):
    eastern = ZoneInfo("America/Toronto")
    now_et = datetime.now(eastern).date()

    db.collection("logs").add(
        {
            "message": message,
            "level": level,
            "timestamp": now_et.strftime("%Y-%m-%d %H:%M:%S %Z"),
        }
    )
