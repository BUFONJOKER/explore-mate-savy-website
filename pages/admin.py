import streamlit as st
from data_frame import BusinessDataFrame, ReviewsDataFrame, UsersDataFrame, UserProfiles,UpdateProfile

# Initialize session state for login status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

st.title("Admin Page")
st.write("Welcome to the admin page.")

if not st.session_state.logged_in:
    st.write("First log in with admin credentials to view the data.")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    

    login_button = st.button("Login")

    if login_button:
        
        if username == "admin" and password == "admin":
            st.session_state.logged_in = True
            st.rerun()
            
        else:
            st.write("Invalid credentials. Please try again.")
else:
    st.write("Login successful!")
    logout_button = st.button(" Logout",icon=":material/logout:")

    if logout_button:
        st.session_state.logged_in = False
        st.switch_page("business_discovery.py")
    st.write("What would you like to do?")

    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        business_data_button = st.button("View Business Data")

    if business_data_button:
        st.write(BusinessDataFrame())

    with col2:
        reviews_data_button = st.button("View Reviews Data")
    
    if reviews_data_button:
        st.write(ReviewsDataFrame())

    with col3:
        users_data_button = st.button("View Users Data")
    
    if users_data_button:
        st.write(UsersDataFrame())

    with col4:
        user_profiles_button = st.button("View User Profiles")
    
    if user_profiles_button:
        st.write(UserProfiles())
        
    
        
    