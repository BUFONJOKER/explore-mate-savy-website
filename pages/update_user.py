import streamlit as st
from data_frame import UserProfiles, UpdateProfile
import re
import pandas as pd
from crypto_utils import encrypt_password, decrypt_password

st.title("Update User Profile")

df = UserProfiles()

if "email" not in st.query_params:
    email = st.session_state.email


elif "email" in st.query_params:
    email = st.query_params.email

# First Name
first_name = df[df['Email'] == email]['FirstName'].values[0]

# Last Name
last_name = df[df['Email'] == email]['LastName'].values[0]

# password
password = df[df['Email'] == email]['Password'].values[0]
password = decrypt_password(password)

# First Name input field
first_name_text = st.text_input("First Name", value=first_name)

# Last Name input field
last_name_text = st.text_input("Last Name", value=last_name)


# Password
password_text = st.text_input("Password", type="password", value=password)

# update button
update = st.button("Update", type="secondary")



if update:
        
        if first_name_text!=first_name:
            df.loc[df['Email'] == email, 'FirstName'] = first_name_text
            
        if last_name_text!=last_name:
            df.loc[df['Email'] == email, 'LastName'] = last_name_text
            
        if password_text!=password:
            df.loc[df['Email'] == email, 'Password'] = encrypt_password(password_text)
                    
        # Update the dataframe with new user data
        update_profile = UpdateProfile(df)
        if update_profile:
                
                st.success("Profile Updated Successfully")
                st.session_state.clear()
                
                st.switch_page("business_discovery.py")
            
            
        