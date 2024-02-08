import streamlit as st


st.title('Your 5 to 9 club')
st.header('Helping you put the life into your work-life balance')
#st.divider()

# Define your columns
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Introduce yourself with your passions instead of job title") 
    st.write("Don't just be Sarah who works at McKinsey, be Sarah who likes pottery, acrylic painting or photography. Don't let your job define your identity.")

with col2:
    st.subheader("Discover classes that fit around your 9 to 5") 
    st.write("Take our 1-minute quiz, and we'll recommend classes, plan your journey from the office, and get you a TooGoodToGo on the way home.")

with col3:
    st.subheader("Trying to meet new people, or make new friends?") 
    st.write("We've curated 40 classes from 1000s accross london. These are designed to be convinient for your professionals, and are great for meeting new people.")



# Button to find classes
if st.button('Find Me Classes'):
    # Use st.markdown to create a clickable link
    st.markdown("[Click here to find classes](https://your5to9-mx4zyntqxwkkrz9f64ejps.streamlit.app/)", unsafe_allow_html=True)

if st.button('Show All Classes'):
    # Use st.markdown to create a clickable link
    st.markdown("[Click here to show all classes](https://app.nocodemapapp.com/map/KPC9LXprRob5i8INbUM6)", unsafe_allow_html=True)
#st.divider()
st.subheader('About Us')

col1, col2= st.columns([0.2, 0.8])
with col1:
    st.image('https://media.licdn.com/dms/image/D4E03AQFgLf0cupxD0w/profile-displayphoto-shrink_200_200/0/1696936875274?e=1712793600&v=beta&t=L3AEc9bNKZ2tNNRiB0tzO50vmINhAdaBtuijpcTgkZs')

with col2:
    st.write("Hi I'm Talvin, I created Your5to9club because I'm tired of having boring conversations at parties. It all started one night at my mates birthday where I was contstanly asked 'so, what do you do?'. I hate that question, and I've much prefer to discuss each others passions, interests and hobbies")

# st.page_link('Discover London', 'https://app.nocodemapapp.com/app/KPC9LXprRob5i8INbUM6')
# st.page_link('Book a class', 'https://app.nocodemapapp.com/app/KPC9LXprRob5i8INbUM6', 'coming soon')
# st.page_link('View all classes', 'https://app.nocodemapapp.com/app/KPC9LXprRob5i8INbUM6')

# if Recommend_classes:
#     # Redirect to a new page
#     st.write('Redirecting to classes...')
#     st.switch_page("C:\\Users\\talvi\Your5to9quiz4.py")
 
# if Show_all_classes:
#     # Redirect to a new page
#     st.write('Redirecting to classes...')
#     st.switch_page("https://app.nocodemapapp.com/app/KPC9LXprRob5i8INbUM6")
