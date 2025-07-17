import json
from scraper import find_tickets
from emails import send_email
from locations import city_to_id


def check_trackers():
    try:
        with open("trackers.json", "r") as f:
            trackers = json.load(f)
    except FileNotFoundError:
        return
    except json.JSONDecodeError:
        return

    if not trackers:
        return

    updated_trackers = []

    for t in trackers:
        tickets = find_tickets(
            origin_id=city_to_id[t["origin"]],
            destination_id=city_to_id[t["destination"]],
            start_date=t["start_date"],
            end_date=t["end_date"],
            total_passengers=t.get["passengers", 1],
            min_price=t.get("min_price"),
            max_price=t["max_price"],
        )

        if tickets:
            send_email(t["email"], tickets)
        else:
            updated_trackers.append(t)  # keep if no match yet

    # save updated list (without the ones that got a match)
    with open("trackers.json", "w") as f:
        json.dump(updated_trackers, f, indent=2)
