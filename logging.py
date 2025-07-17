from google.cloud import firestore
import streamlit as st
from datetime import datetime
import pytz

# set up logging
db = firestore.Client.from_service_account_info(st.secrets["firebase"])


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
