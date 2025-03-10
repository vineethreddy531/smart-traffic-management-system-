import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import uuid

# Set up page configuration
st.set_page_config(page_title="Carpooling App", layout="wide")

# Load or initialize datasets
try:
    ride_data = pd.read_csv("book_ride.csv")
except FileNotFoundError:
    ride_data = pd.DataFrame(columns=["ride_id", "user_id", "origin", "destination", "date", "time", "price", "reviews"])

try:
    offer_data = pd.read_csv("offer_ride.csv")
except FileNotFoundError:
    offer_data = pd.DataFrame(columns=["ride_id", "user_id", "origin", "destination", "date", "time", "price", "vehicle", "seats_available"])

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Register", "Login", "Book a Ride", "Offer a Ride", "Reviews"])

# Home Page
if page == "Home":
    st.title("🚗 Carpooling App")
    st.image("logo.jpg", use_column_width=True)
    st.write("Welcome to the Carpooling App! Find or offer rides easily.")

# Registration Page
elif page == "Register":
    st.title("Register")
    user_id = str(uuid.uuid4())
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    if st.button("Register"):
        st.success("Registered Successfully! Your User ID: " + user_id)

# Login Page
elif page == "Login":
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        st.success("Logged in Successfully!")

# Book a Ride
elif page == "Book a Ride":
    st.title("Book a Ride")
    origin = st.text_input("Enter Origin City")
    destination = st.text_input("Enter Destination City")
    date = st.date_input("Select Date")
    if st.button("Search Rides"):
        filtered_rides = ride_data[(ride_data["origin"].str.lower() == origin.lower()) & 
                                   (ride_data["destination"].str.lower() == destination.lower())]
        if not filtered_rides.empty:
            st.write(filtered_rides)
            ride_id = st.selectbox("Select Ride", filtered_rides["ride_id"])
            if st.button("Book Ride"):
                st.success(f"Ride {ride_id} booked successfully!")
        else:
            st.error("No rides available for this route.")
    
    # Map Integration
    st.subheader("Ride Map")
    map_center = [20.5937, 78.9629]
    map = folium.Map(location=map_center, zoom_start=5)
    folium.Marker(location=map_center, popup="Ride Location", icon=folium.Icon(color="blue")).add_to(map)
    folium_static(map)

# Offer a Ride
elif page == "Offer a Ride":
    st.title("Offer a Ride")
    ride_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())
    origin = st.text_input("Enter Origin City")
    destination = st.text_input("Enter Destination City")
    date = st.date_input("Select Date")
    time = st.time_input("Select Time")
    price = st.number_input("Enter Price (INR)", min_value=0)
    vehicle = st.text_input("Enter Vehicle Details")
    seats = st.number_input("Available Seats", min_value=1, max_value=10)
    if st.button("Offer Ride"):
        new_ride = pd.DataFrame([[ride_id, user_id, origin, destination, date, time, price, vehicle, seats]],
                                columns=["ride_id", "user_id", "origin", "destination", "date", "time", "price", "vehicle", "seats_available"])
        offer_data = pd.concat([offer_data, new_ride], ignore_index=True)
        offer_data.to_csv("offer_ride.csv", index=False)
        st.success(f"Ride Offered Successfully! Ride ID: {ride_id}")
    
    # Map Integration for Offered Ride
    st.subheader("Ride Map")
    map_center = [20.5937, 78.9629]
    map = folium.Map(location=map_center, zoom_start=5)
    folium.Marker(location=map_center, popup="Ride Start Location", icon=folium.Icon(color="green")).add_to(map)
    folium_static(map)

# Reviews Section
elif page == "Reviews":
    st.title("Reviews & Ratings")
    ride_id = st.text_input("Enter Ride ID to Review")
    rating = st.slider("Rate the Ride", 1, 5)
    review_text = st.text_area("Write a Review")
    if st.button("Submit Review"):
        ride_data.loc[ride_data["ride_id"] == ride_id, "reviews"] = f"Rating: {rating}, {review_text}"
        ride_data.to_csv("book_ride.csv", index=False)
        st.success("Review Submitted!")
