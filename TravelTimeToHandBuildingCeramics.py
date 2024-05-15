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
st.set_page_config(page_title="The 5 to 9 Club travel time widget", page_icon="🗺️", layout="centered")
st.title("The 5 to 9 Club travel time widget")
st.write("Enter your office and home address to calculate the travel time to this Hand Building Ceramics Course")

# Input field for the user's office address
office_address = st.text_input("Office Address e.g. 1 bedford row")
home_address = st.text_input("Home Address e.g. IG2 5IO")

# Calculate button
if st.button('Calculate Travel Time'):
    if office_address:
        with st.spinner('Calculating...'):
            travel_time = calculate_travel_time(office_address, "Art Hub Studios - Building 28, Westminster Industrial Estate, Unit 2b, 34 Bowater Rd, London, SE18 5TF")
            if travel_time is not None:
                st.success(f"The travel time from your office is:{travel_time} minutes.")
            else:
                st.error("Unable to calculate travel time. Please check the address and try again.")
    if home_address:
        with st.spinner('Calculating...'):
            travel_time = calculate_travel_time(home_address, "Art Hub Studios - Building 28, Westminster Industrial Estate, Unit 2b, 34 Bowater Rd, London, SE18 5TF")
            if travel_time is not None:
                st.success(f"The travel time from your home is: {travel_time} minutes.")
            else:
                st.error("Unable to calculate travel time. Please check the address and try again.")            
    else:
        st.error("Please enter a home or office address.")
