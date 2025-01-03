import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
from data_frame import UserProfiles

# # establish connection to Google Sheets

# conn = st.connection("gsheets", type=GSheetsConnection)

# # fetch existing data
# existing_data = conn.read(worksheet="UserProfiles")
# st.dataframe(existing_data)

st.write(UserProfiles())
