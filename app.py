import streamlit as st 
from datetime import date 
from scraper import find_tickets
from locations import city_to_id

st.set_page_config(page_title="Megabus Price Tracker", layout="centered")
st.title("🚌 Megabus Price Tracker")
st.markdown("Track ticket prices between cities and find the cheapest fares available.")


# user input
col1, col2 = st.columns(2)
with col1: 
    origin = st.selectbox("Origin City", sorted(city_to_id.keys()))
with col2:
    destination = st.selectbox("Destination City", sorted(city_to_id.keys()))

date_range = st.date_input(
    "Select Date Range",
    [date(2025, 7, 16), date(2025, 7, 18)],
    min_value=date.today()
)

total_passengers = st.number_input(
    "Total Passengers", min_value=1, max_value=10, value=1
)
max_price = st.number_input("Max Price ($CAD)", min_value=1.0, value=100.0)

# search
if st.button("🔍 Search for Tickets"):
    if origin == destination:
        st.warning("Origin and destination must be different.")
    else:
        with st.spinner("Fetching tickets..."):
            tickets = find_tickets(
                origin_id=city_to_id[origin],
                destination_id=city_to_id[destination],
                start_date=str(date_range[0]),
                end_date=str(date_range[1]),
                total_passengers=total_passengers,
                max_price=max_price,
            )

        if tickets:
            st.success(f"Found {len(tickets)} matching tickets!")
            st.dataframe(tickets)
        else:
            st.error("No tickets found under your price limit.")