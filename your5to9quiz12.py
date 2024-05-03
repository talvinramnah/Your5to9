import streamlit as st
import pandas as pd
import googlemaps
from googlemaps.exceptions import ApiError, TransportError, Timeout

# Initialize Google Maps client
gmaps = googlemaps.Client(key='AIzaSyCxtHfoUzG4J8NdqZ60uk8FaU_v50iXwk4')

def get_random_activities():
    try:
        df = pd.read_csv("https://raw.githubusercontent.com/talvinramnah/Your5to9/main/5to9clubDatabase5.csv")
        df = df[['Image link', 'Event name', 'Price', 'Number of Sessions', 'Location', 'Price per week', 'Day and Time', 'tracking link']]
        return df.sample(7)
    except Exception as e:
        st.error(f"Failed to load activities: {e}")
        return pd.DataFrame()

def calculate_travel_time(origin, destination):
    try:
        directions_result = gmaps.directions(origin, destination, mode="transit")
        if directions_result:
            return int(directions_result[0]['legs'][0]['duration']['value'] / 60)  # Save as integer
        else:
            return float('inf')  # Use infinity for unavailable to maintain numeric consistency
    except (ApiError, TransportError, Timeout) as e:
        st.error(f"Google Maps API Error: {e}")
        return float('inf')  # Use infinity for API errors
    except Exception as e:
        st.error(f"Unexpected Error: {e}")
        return float('inf')

def add_travel_times(df, home_address, office_address):
    df['Travel Time from Home'] = df['Location'].apply(lambda x: calculate_travel_time(home_address, x))
    df['Travel Time from Office'] = df['Location'].apply(lambda x: calculate_travel_time(office_address, x))
    return df

def prepare_display_dataframe(home_address, office_address):
    activities_df = get_random_activities()
    if not activities_df.empty:
        activities_df = add_travel_times(activities_df, home_address, office_address)
        return activities_df
    else:
        return pd.DataFrame()

st.title('Find the perfect activity for your personality and your working schedule!')
st.subheader('Answer 8 questions to reveal your perfect activity')

with st.form('quiz'):
    st.markdown("""
    <style>
    .stRadio > label {
        font-size: 16px;
        font-weight: bold;
    }
    .stRadio > div > div {
        text-align: center;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

    tube_line = st.radio(
        'If you were a tube line, which would it be?',
        ['Fiery and Fearless like the Bakerloo line', 'Bold and Balanced like the Central line', 'Adventurous and Analytical like the Circle line', 'Serene and Spontaneous like the District line', 'Daring and Deliberate like the Hammersmith & City line', 'Magnetic and Meticulous like the Jubilee line', 'Sly and Structured like the Metropolitan line', 'Intense and Independent like the Northern line', 'Sensual and Sensible like the Piccadilly line', 'Regal and Resourceful like the Victoria line', 'Efficient and Eccentric like the Waterloo & City line', 'Futuristic and Free-spirited like the DLR', 'Versatile and Vibrant like the London Overground', 'Easygoing and Eccentric like the Tram', 'Modern and Methodical like the TfL Rail', 'Innovative and Independent like the Elizabeth Line', 'Unconventional and Unpredictable because I do not live on a tube line']
    )

    lunch_spot = st.radio(
        'If you were a London lunch spot, what would you be?',
        ['Efficient and Organized like Pret A Manger', 'Zen and Balanced like Itsu', 'Energetic and Vibrant like Leon', 'Spicy and Bold like Wasabi', 'Practical and Budget-conscious like Tesco', 'Sophisticated and Elegant like Marks And Spencers', 'Practical and Dependable like Boots', 'Down-to-earth and Comforting like Greggs', 'Resourceful and Independent because I got my life together and bring it from home', 'Other']
    )

    coffee_spot = st.radio(
        'If you were a coffee shop, what would you be?',
        ['Trendy and Social like Starbucks', 'Warm and Welcoming like Costa', 'Artistic and Bohemian like Cafe Nero', 'Efficient and Organized like Pret A Manger', 'Down-to-earth and Comforting like Greggs', 'Hipster and Edgy like Blank Street', 'Elegant and Refined like Rosslyn', 'chilled out and relaxed because I do not drink coffee', 'Other']
    )

    wfh_schedule = st.multiselect(
        'What days do you normally WFH?',
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    )

    weekend_activity = st.radio(
        'What is your fave weekend vibe?',
        ['Sociable and Lively like Brunch with friends', 'Intellectual and Cultured like Museum visit', 'Adventurous and Thrill-seeking like Outdoor adventure', 'Fashion-forward and Trendy like Shopping spree', 'Tranquil and Peaceful like Relaxing at home', 'Other']
    )

    introvert_or_extrovert = st.radio(
        'Are you an introvert or extrovert?',
        ['Introvert', 'Extrovert']
    )

    office_address = st.text_input('Enter your office address (we do not save any user data)')
    home_address = st.text_input('Enter your home address (we do not save any user data)')
    sort_preference = st.selectbox('Sort results by travel time from:', ['Office', 'Home'])
    submit = st.form_submit_button('Submit')

if submit:
    with st.spinner('Let him cook...'):
        activities_df = prepare_display_dataframe(home_address, office_address)
        st.balloons()
        if not activities_df.empty:
            sort_column = 'Travel Time from Office' if sort_preference == 'Office' else 'Travel Time from Home'
            activities_df = activities_df.sort_values(by=sort_column, na_position='last')  # Sort by travel time, treating 'inf' as last

            for _, row in activities_df.iterrows():
                # HTML structure for each card
                card_html = f"""
                <div style="display: flex; margin-bottom: 20px; border: 1px solid #ccc; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                    <div style="min-width: 160px;">
                        <img src="{row['Image link']}" alt="{row['Event name']}" style="width: 160px; height: 160px; object-fit: cover;">
                    </div>
                    <div style="padding: 10px; flex-grow: 1; display: flex; justify-content: space-between;">
                        <div>
                            <h4>{row['Event name']}</h4>
                            <p>{row['Day and Time']}</p>
                            <p>{row['Location']}</p>
                            <p>Price per session: {row['Price']}</p>
                            <p>Price per week: {row['Price per week']}</p>
                            <p>Total sessions: {row['Number of Sessions']}</p>
                        </div>
                        <div>
                            <p>Travel from Home: {row['Travel Time from Home']} min</p>
                            <p>Travel from Office: {row['Travel Time from Office']} min</p>
                        </div>
                    </div>
                    <a href="{row['tracking link']}" target="_blank" style="text-decoration: none; color: white; background-color: #007bff; border: none; padding: 10px 20px; border-radius: 5px; font-weight: bold; margin: 10px; align-self: flex-end;">Book Now</a>
                </div>
                """


                st.markdown(card_html, unsafe_allow_html=True)
        else:
            st.write('No activities found.')
