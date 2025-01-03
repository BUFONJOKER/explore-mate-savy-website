import streamlit as st
from data_frame import UserProfiles
from crypto_utils import encrypt_password, decrypt_password



st.cache_data.clear()
df = UserProfiles()

# Longin Page 
st.title("Login")

# email 
email = st.text_input("Email")

# password
password = st.text_input("Password", type="password")

login = st.button("Login",icon=":material/login:")
if login:
    if df['Email'].str.contains(email).any():
        encrypted_password = df.loc[df['Email'] == email, 'Password'].values[0]
        decrypt_password = decrypt_password(encrypted_password)
        if password == decrypt_password:
            st.success("Login Successful")
            st.write("Go to main page")
            st.session_state.email = email
            st.switch_page("business_discovery.py")
        else:
            st.error("Invalid Password")
        
    else:
        st.error("Invalid Email")

if not login:
    st.header("Don't have an account?")
    st.write("Create an account")
    signup_button = st.button("👥 Sign Up")
    if signup_button:
        st.switch_page("pages/signup.py")