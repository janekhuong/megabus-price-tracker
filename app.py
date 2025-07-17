import streamlit as st
from datetime import date
from scraper import find_tickets
from locations import city_to_id
from emails import test_email_send

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
        origin = st.selectbox(
            "From", ["Enter a town or city"] + locations)

    with col2:
        destination_options = [city for city in locations if city != origin]
        destination = st.selectbox("To", ["Enter a town or city"] + destination_options)

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

    # st.markdown("<div style='padding-top: 20px;'></div>", unsafe_allow_html=True)

    if st.button("Submit", use_container_width=True):
        if origin == "Enter a town or city":
            st.warning("Please select origin town or city")
        elif destination == "Enter a town or city":
            st.warning("Please select desitnation town or city")
        elif not date_range:
            st.warning("Please enter a date")
        elif origin == destination:
            st.warning("Origin and destination must be different.")
        else:
            st.session_state.submitted = True
            start 
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
