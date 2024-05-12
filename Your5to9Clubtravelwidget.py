import streamlit as st
import googlemaps
from googlemaps.exceptions import ApiError, TransportError, Timeout

# Initialize Google Maps client
gmaps = googlemaps.Client(key='AIzaSyCxtHfoUzG4J8NdqZ60uk8FaU_v50iXwk4')

def calculate_travel_time(origin, destination):
    try:
        directions_result = gmaps.directions(origin, destination, mode="transit")
        if directions_result:
            return int(directions_result[0]['legs'][0]['duration']['value'] / 60)  # Return travel time in minutes
        else:
            return None
    except (ApiError, TransportError, Timeout) as e:
        st.error(f"Google Maps API Error: {e}")
        return None
    except Exception as e:
        st.error(f"Unexpected Error: {e}")
        return None

# Streamlit UI
st.set_page_config(page_title="Travel Time Calculator", page_icon="🗺️", layout="centered")
st.title("Calculate Travel Time to Make Town")
st.write("Enter your office address to calculate the travel time to Make Town - 32 Vyner Street, London, E2 9DQ, England.")

# Input field for the user's office address
office_address = st.text_input("Office Address")

# Calculate button
if st.button('Calculate Travel Time'):
    if office_address:
        with st.spinner('Calculating...'):
            travel_time = calculate_travel_time(office_address, "Make Town - 32 Vyner Street, London, E2 9DQ, England")
            if travel_time is not None:
                st.success(f"The estimated travel time from your office to Make Town is {travel_time} minutes.")
            else:
                st.error("Unable to calculate travel time. Please check the address and try again.")
    else:
        st.error("Please enter an office address.")
