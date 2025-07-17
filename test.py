from scraper import find_tickets
from emails import send_email

# results = find_tickets(
#     origin_id=145,
#     destination_id=280,
#     start_date="2025-07-16",
#     end_date="2025-07-18",
#     total_passengers=1,
#     min_price=80,
#     max_price=85,
# )

# print(results)

# sample_tickets = [
#     {
#         "date": "2025-07-16",
#         "price": 29.99,
#         "departureTime": "10:00",
#         "arrivalTime": "14:00",
#     },
#     {
#         "date": "2025-07-17",
#         "price": 25.00,
#         "departureTime": "12:30",
#         "arrivalTime": "16:45",
#     },
# ]

# send_email("janek170805@gmail.com", sample_tickets)
