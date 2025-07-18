import streamlit as st
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import pytz

# set up logging
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def log_event(message, level="INFO"):
    eastern = pytz.timezone("US/Eastern")
    now_et = datetime.now(pytz.utc).astimezone(eastern)

    db.collection("logs").add(
        {
            "message": message,
            "level": level,
            "timestamp": now_et.strftime("%Y-%m-%d %H:%M:%S %Z"),
        }
    )
