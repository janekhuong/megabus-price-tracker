import streamlit as st
from datetime import date
from scraper import find_tickets
from locations import city_to_id
from emails import test_email_send

st.set_page_config(page_title="Megabus Price Tracker", layout="centered")

st.markdown(
    """
 <style>
 .stApp {
 background-color: #001779;
 }
 </style>
 """,
    unsafe_allow_html=True,
)

st.markdown(
    "<h1 style='text-align: center; color: white;'>🚌 Megabus Price Tracker</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: white'>Enter details of a Megabus trip you'd like to track and we'll send you an email when a matching ticket is found!</p>",
    unsafe_allow_html=True,
)

st.markdown(
    """
 <style>
 /* General label styling */
label {
 color: white !important;
}

 /* Target all Streamlit buttons */
 .stButton > button {
 background-color: #f9be2c;
 color: #001779;
 border: none;
 border-radius: 4px;
 cursor: pointer;
 transition: background-color 0.3s ease;
 }

 /* Hover effect */
 .stButton > button:hover {
 background-color: #fac645;
 color: #001779;
 }

 </style>
""",
    unsafe_allow_html=True,
)

# user input
col1, col2 = st.columns(2)
with col1:
    origin = st.selectbox(
        "From", ["Enter a town or city"] + sorted(city_to_id.keys())
    )

with col2:
    destination = st.selectbox(
        "To", ["Enter a town or city"] + sorted(city_to_id.keys())
    )

date_range = st.date_input(
    "Leaving", [], min_value=date.today()
)

total_passengers = st.number_input(
    "How many travelers?", min_value=1, max_value=10, value=1
)

col1, col2 = st.columns(2)

with col1:
    min_price = st.number_input("Min price", min_value=0.0, value=20.0, step=1.0)

with col2:
    max_price = st.number_input(
        "Max price", min_value=min_price, value=100.0, step=1.0
    )

# search

st.markdown("<div style='padding-top: 20px;'></div>", unsafe_allow_html=True)

if st.button("Submit", use_container_width=True):
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
