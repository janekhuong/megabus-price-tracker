import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from zoneinfo import ZoneInfo
from scraper import find_tickets
from emails import send_email
from locations import city_to_id
from app_logging import log_event

if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()


def check_trackers():
    trackers_ref = db.collection("trackers")
    docs = list(trackers_ref.stream())

    if not docs:
        log_event("No trackers to process. Exiting.")
        return

    eastern = ZoneInfo("America/Toronto")
    today = datetime.now(eastern).date()

    for doc in docs:
        t = doc.to_dict()
        doc_id = doc.id

        try:
            end_date = datetime.strptime(t["end_date"], "%Y-%m-%d").date()
            if end_date < today:
                trackers_ref.document(doc_id).delete()
                log_event(
                    f"Deleted expired tracker ending on {t['end_date']} for {t['email']}"
                )
                continue
        except Exception as e:
            log_event(
                f"Error parsing date or deleting expired tracker: {e}", level="ERROR"
            )
            continue

        tickets = find_tickets(
            origin_id=city_to_id[t["origin"]],
            destination_id=city_to_id[t["destination"]],
            start_date=t["start_date"],
            end_date=t["end_date"],
            total_passengers=t.get("passengers", 1),
            min_price=t.get("min_price"),
            max_price=t["max_price"],
        )

        if tickets:
            send_email(t["email"], tickets)
            trackers_ref.document(doc_id).delete()
            log_event(f"Sent email and deleted matched tracker for {t['email']}")
