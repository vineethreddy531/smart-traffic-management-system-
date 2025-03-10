import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd

# Set page title & layout
st.set_page_config(page_title="Carpooling App", layout="wide")

# CSV Files for Data Storage
offer_ride_file = "offer_ride.csv"
book_ride_file = "book_ride.csv"

# 📍 Predefined coordinates for major cities in India
city_coordinates = {
    "hyderabad": (17.3850, 78.4867),
    "mumbai": (19.0760, 72.8777),
    "delhi": (28.7041, 77.1025),
    "bangalore": (12.9716, 77.5946),
    "chennai": (13.0827, 80.2707),
    "kolkata": (22.5726, 88.3639),
    "pune": (18.5204, 73.8567),
}

def get_lat_lon(location):
    location = location.lower()
    return city_coordinates.get(location, (None, None))

# --- Sidebar Navigation ---
st.sidebar.title("🚗 Carpooling App")
page = st.sidebar.radio("Go to", ["Home", "Register", "Login", "Book a Ride", "Offer a Ride"])

# --- Home Page ---
if page == "Home":
    st.markdown("<h1 style='text-align: center;'>Welcome to Carpooling App</h1>", unsafe_allow_html=True)
    st.image("logo.jpg", use_container_width=True)
    
    st.markdown(
        """
        ### **🌍 Share Rides, Save Costs, & Travel Together!**  
        - Offer a ride to help others & split travel costs.  
        - Book a ride easily from available options.  
        - Track your rides live with real-time map updates.  
        """, unsafe_allow_html=True
    )

# --- Registration Page ---
elif page == "Register":
    st.header("📝 Register for Carpooling")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    password = st.text_input("Password", type="password")
    car_details = st.text_input("Car Model (Optional)")
    seats_offered = st.number_input("Seats Available in Car (if offering rides)", min_value=1, max_value=10, step=1)

    if st.button("Register"):
        st.success("Registration Successful! You can now log in.")

# --- Login Page ---
elif page == "Login":
    st.header("🔑 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        st.success(f"Welcome back, {email}!")

# --- Book a Ride ---
elif page == "Book a Ride":
    st.header("📍 Book a Ride")

    try:
        ride_data = pd.read_csv(book_ride_file)
    except FileNotFoundError:
        st.warning("No ride data found. Please check back later.")
        ride_data = pd.DataFrame(columns=["user", "origin", "destination", "time", "seats", "price", "status"])

    origin = st.text_input("From (Origin)")
    destination = st.text_input("To (Destination)")
    date = st.date_input("Travel Date")

    if st.button("Search Rides"):
        filtered_rides = ride_data[
            (ride_data["origin"].str.lower().str.contains(origin.lower(), na=False)) &
            (ride_data["destination"].str.lower().str.contains(destination.lower(), na=False))
        ]

        if not filtered_rides.empty:
            st.write("### Available Rides")
            for index, row in filtered_rides.iterrows():
                st.write(f"🚘 **{row['origin']} → {row['destination']}** at {row['time']} | 💺 Seats: {row['seats']} | ₹ {row['price']} | Status: {row['status']}")
                if st.button(f"Book Ride {index}"):
                    ride_data.at[index, "status"] = "Booked"
                    ride_data.to_csv(book_ride_file, index=False)
                    st.success("Ride Booked Successfully!")
        else:
            st.warning("No matching rides found. Try another location or time.")

# --- Offer a Ride ---
elif page == "Offer a Ride":
    st.header("🚘 Offer a Ride")

    origin = st.text_input("Start Location")
    destination = st.text_input("End Location")
    date = st.date_input("Travel Date")
    time = st.time_input("Departure Time")
    seats = st.number_input("Available Seats", min_value=1, max_value=10, step=1)
    price = st.number_input("Price per Seat (INR)", min_value=0.0, step=50.0)

    if st.button("Post Ride"):
        new_ride = pd.DataFrame([{ "origin": origin, "destination": destination, "time": str(time), "seats": seats, "price": price, "status": "Available" }])
        try:
            existing_data = pd.read_csv(offer_ride_file)
            updated_data = pd.concat([existing_data, new_ride], ignore_index=True)
        except FileNotFoundError:
            updated_data = new_ride
        updated_data.to_csv(offer_ride_file, index=False)
        st.success("Your ride has been posted successfully!")

    # --- Map Integration ---
    st.subheader("Route Map")
    lat1, lon1 = get_lat_lon(origin)
    lat2, lon2 = get_lat_lon(destination)

    if lat1 and lat2:
        m = folium.Map(location=[(lat1 + lat2) / 2, (lon1 + lon2) / 2], zoom_start=6)
        folium.Marker([lat1, lon1], popup=f"{origin} (Start)", icon=folium.Icon(color="blue")).add_to(m)
        folium.Marker([lat2, lon2], popup=f"{destination} (Destination)", icon=folium.Icon(color="red")).add_to(m)
        folium.PolyLine([(lat1, lon1), (lat2, lon2)], color="green", weight=5).add_to(m)
        folium_static(m)
    else:
        st.warning("Invalid city name. Please enter a major city from the list.")
