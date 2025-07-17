import json
import time
from datetime import date
from scraper import find_tickets
from emails import send_email
from locations import city_to_id


def check_trackers():
    try:
        with open("trackers.json", "r") as f:
            trackers = json.load(f)
    except FileNotFoundError:
        trackers = []

    updated_trackers = []

    for t in trackers:
        tickets = find_tickets(
            origin_id=city_to_id[t["origin"]],
            destination_id=city_to_id[t["destination"]],
            start_date=t["start_date"],
            end_date=t["end_date"],
            total_passengers=t["passengers"],
            min_price=t.get("min_price"),
            max_price=t["max_price"],
        )

        if tickets:
            send_email(t["email"], tickets)
            print(f"🎉 Match found for {t['email']}, email sent.")
            # Do NOT add this tracker to the updated list (removes it)
        else:
            updated_trackers.append(t)  # Keep if no match yet

    # Save updated list (without the ones that got a match)
    with open("trackers.json", "w") as f:
        json.dump(updated_trackers, f, indent=2)


# Run every 60 minutes
while True:
    check_trackers()
    time.sleep(3600) 
