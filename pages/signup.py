import streamlit as st
import re
import pandas as pd
from data_frame import UserProfiles
from data_frame import CreateProfile
from crypto_utils import decrypt_password, encrypt_password





df = UserProfiles()

st.title("Sign Up")

st.markdown("Please fill out the form below to sign up.")

# First Name
first_name = st.text_input("First Name")

# Last Name
last_name = st.text_input("Last Name")

# Email input field
email = st.text_input("Enter your email")


# Password
password = st.text_input("Password", type="password")
password = encrypt_password(password)
# Visited Place
visited_place = ""

# Liked Place
liked_place = ""
# SignUp button
sign_up = st.button("👥 Sign Up", type="secondary")

if sign_up:
    # Email validation function
    def is_valid_email(email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email)

    # Check email validity

    if not is_valid_email(email):
        st.error("Invalid email address. Please try again.")
    
    elif is_valid_email(email):
        
        # Check if all fields are filled
        if first_name and last_name and email and password:
            
            # Check if user already exists
            
            if df['Email'].str.contains(email).any():
                st.error("Email Already exist")
                st.stop()
            
            if df['Password'].str.contains(password).any():
                st.error("Password Already exist")
                st.stop()
            
            else:
                
                
                
                # create new user
                new_user = pd.DataFrame(
                [
                    {
                    "FirstName": first_name,
                    "LastName": last_name,
                    "Email": email,
                    "Password": password,
                    "VisitedPlaces": visited_place,
                    "LikedPlaces": liked_place
                    }
                ]
                )
                
                # Update the dataframe with new user data
                updated_df = pd.concat([df, new_user], ignore_index=True)
                user_created = CreateProfile(updated_df)
                if user_created:
                    st.success("Profile Created Successfully")
                    st.write("Please login to continue.")
                    st.switch_page("pages/login.py")
                    
        else:
            st.error("Please fill out all the fields.")








