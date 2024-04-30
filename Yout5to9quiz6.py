import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import googlemaps
import pandas as pd
import time
from googlemaps.exceptions import ApiError, TransportError, Timeout

# Initialize Google Maps client
gmaps = googlemaps.Client(key='AIzaSyCxtHfoUzG4J8NdqZ60uk8FaU_v50iXwk4')


def get_class_info():
    try:
        # Use the raw GitHub URL of your CSV file
        csv_url = "https://raw.githubusercontent.com/talvinramnah/Your5to9/main/5to9club%20database2.csv"
        df = pd.read_csv(csv_url)
        return df.to_dict('records')  # Convert DataFrame to a list of dictionaries
    except Exception as e:
        st.error(f"Failed to load class info: {e}")
        return []


def calculate_travel_time(origin, destination):
    try:
        directions_url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&mode=transit&key=Your_Google_Maps_API_Key"
        print("Request URL (API Key omitted):", directions_url.replace("Your_Google_Maps_API_Key", "API_KEY_OMITTED"))
        directions_result = gmaps.directions(origin, destination, mode="transit")
        if directions_result:
            travel_time = directions_result[0]['legs'][0]['duration']['value'] / 60
            return travel_time
    except Exception as e:
        print(f"Full error: {e}")
    return None


def recommend_classes(user_address, selected_themes):
    try:
        # Load class information from a local file (CSV or JSON)
        class_info = get_class_info()
        recommended_classes = []

        # Iterate through each class to check if it matches the selected themes and is within 30 minutes travel time
        for row in class_info:
            # Check if the class theme matches any of the selected themes, or if no themes are selected
            if not selected_themes or row['Theme'] in selected_themes:
                # Calculate travel time from the user address to the class location
                travel_time = calculate_travel_time(user_address, row['Location'])
                # If the travel time is 30 minutes or less, add the class to the list of recommendations
                if travel_time and travel_time <= 30:
                    recommended_classes.append(row)

        # Convert the list of recommended classes into a DataFrame
        if recommended_classes:
            recommendations_df = pd.DataFrame(recommended_classes)
            return recommendations_df
        else:
            # Return an empty DataFrame if no classes meet the criteria
            return pd.DataFrame()
    except Exception as e:
        # Display an error message in Streamlit if an exception occurs
        st.error(f"Failed to recommend classes: {e}")
        return pd.DataFrame()

st.title('The 5 To 9 Club Personality Test')
st.subheader('Answer these questions and find out what arts classes match your personality and 9-5 schedule')

with st.form('quiz'):
    address = st.text_input('Enter your office address')
    selected_themes = st.multiselect('What classes are you interested in?', ['Pottery', 'Textiles', 'Arts and crafts', 'Dancing', 'Jewellery', 'Photography'])
    submit = st.form_submit_button('Submit')
    
    if submit:
        with st.spinner('Finding classes within 30 minutes of your office...'):
            # Pass the selected themes to the recommend_classes function
            recommendations_df = recommend_classes(address, selected_themes)
            if not recommendations_df.empty:
                st.subheader('Recommended Classes Near You:')
                st.dataframe(recommendations_df)
            else: 
                st.write('No classes found within 30 minutes travel time.')
