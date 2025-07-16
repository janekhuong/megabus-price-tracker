import requests
from datetime import datetime, timedelta
from locations import city_to_id

def find_tickets(
    origin_id, destination_id, start_date, end_date, total_passengers=1, max_price=None
):
    url = "https://ca.megabus.com/journey-planner/api/journeys"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": "https://ca.megabus.com/",
    }

    results = []
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")

    while current_date <= end_dt:
        departure_str = current_date.strftime("%Y-%m-%d")

        params = {
            "originId": origin_id,
            "destinationId": destination_id,
            "departureDate": departure_str,
            "totalPassengers": total_passengers,
            "concessionCount": 0,
            "nusCount": 0,
            "otherDisabilityCount": 0,
            "wheelchairSeated": 0,
            "pcaCount": 0,
            "days": 1,
            "carrierId": 16,
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            for journey in data.get("journeys", []):
                price_info = journey.get("price")
                if isinstance(price_info, dict):
                    price = price_info.get("total")
                else:
                    price = price_info

                if price is None:
                    continue

                if max_price is None or price <= max_price:
                    results.append(
                        {
                            "date": departure_str,
                            "departureTime": journey["departureDateTime"],
                            "arrivalTime": journey["arrivalDateTime"],
                            "price": price,
                        }
                    )

        except Exception as e:
            print(f"Failed to fetch {departure_str}: {e}")

        current_date += timedelta(days=1)

    return results


# Toronto (145) → Montreal (280), from July 16 to 18, max $30
tickets = find_tickets(
    origin_id=city_to_id["Toronto, ON"],
    destination_id=city_to_id["Montreal, QC"],
    start_date="2025-07-16",
    end_date="2025-07-18",
    total_passengers=1,
    max_price=100,
)
for t in tickets:
    print(f"{t['date']}: ${t['price']} | {t['departureTime']} → {t['arrivalTime']}")
