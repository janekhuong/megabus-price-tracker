import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import date
from locations import city_to_id

if not firebase_admin._apps:
    cred = credentials.Certificate("firebase/firebase-key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()


def save_tracking_config(
    origin, destination, start_date, end_date, passengers, min_price, max_price, email
):

    entry = {
        "origin": origin,
        "destination": destination,
        "start_date": str(start_date),
        "end_date": str(end_date),
        "passengers": passengers,
        "min_price": min_price,
        "max_price": max_price,
        "email": email,
    }

    db.collection("trackers").add(entry)


st.set_page_config(page_title="Megabus Price Tracker", layout="centered")

# Initialize session state for submission
if "submitted" not in st.session_state:
    st.session_state.submitted = False

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
    display: block;
    margin-left: auto;
    margin-right: auto;
    margin-top: 20px;
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

if not st.session_state.submitted:

    st.markdown(
        "<h1 style='text-align: center; color: white;'>🚌 Megabus Price Tracker</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; color: white'>Enter details of a Megabus trip you'd like to track and we'll send you an email when a matching ticket is found!</p>",
        unsafe_allow_html=True,
    )

    # user input

    locations = sorted(city_to_id.keys())

    col1, col2 = st.columns(2)
    with col1:
        origin = st.selectbox("From", ["Enter a town or city"] + locations)

    with col2:
        destination_options = [city for city in locations if city != origin]
        destination = st.selectbox("To", ["Enter a town or city"] + destination_options)

    date_range = st.date_input("Leaving", [], min_value=date.today())

    total_passengers = st.number_input(
        "How many travelers?", min_value=1, max_value=10, value=1
    )

    col1, col2 = st.columns(2)

    with col1:
        min_price = st.number_input("Min price", min_value=0.0, step=1.0)

    with col2:
        max_price = st.number_input("Max price", min_value=min_price, step=1.0)

    email = st.text_input("Email", placeholder="you@example.com")

    if st.button("Submit", use_container_width=True):
        if origin == "Enter a town or city":
            st.warning("Please select origin town or city")
        elif destination == "Enter a town or city":
            st.warning("Please select destination town or city")
        elif len(date_range) != 2:
            st.warning("Please select a start and end date")
        elif "@" not in email or "." not in email:
            st.warning("Please enter a valid email address")
        else:
            save_tracking_config(
                origin,
                destination,
                date_range[0],
                date_range[1],
                total_passengers,
                min_price,
                max_price,
                email,
            )
            st.session_state.submitted = True
            st.rerun()
else:
    st.markdown(
        "<h1 style='text-align: center; color: white;'>You're all set!</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; color: white'>We'll send you an email when a ticket that matches your criteria is available.</p>",
        unsafe_allow_html=True,
    )

    if st.button("Track another trip"):
        st.session_state.submitted = False
        st.rerun()
