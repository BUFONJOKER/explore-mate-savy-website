import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection


# establish connection to Google Sheets
user_profiles = st.connection("gsheets_userProfiles", type=GSheetsConnection)
business_data = st.connection("gsheets_businessData", type=GSheetsConnection)
reviews_data = st.connection("gsheets_reviewsData", type=GSheetsConnection)
user_data = st.connection("gsheets_userData", type=GSheetsConnection)

# Function to return the dataframe to other pages
def BusinessDataFrame():
    # df = pd.read_csv("business_df_after_more_clean.csv") 
    df = business_data.read(worksheet="business")
    return df

def ReviewsDataFrame():
    # df = pd.read_csv("reviews.csv")
    df = reviews_data.read(worksheet="reviews")
    return df

def UsersDataFrame():
    
    # df = pd.read_csv("yelp_user_data_cleaned.csv")
    df = user_data.read(worksheet="user")
    return df


def UserProfiles():
    
    # fetch existing data
    df = user_profiles.read(worksheet="user_profile")
    # df = pd.read_csv("random_user_profiles_data.csv")
    return df

def CreateProfile(new_user):

    updated = new_user
    user_profiles.update(worksheet="user_profile", data=updated)
    # updated.to_csv("random_user_profiles_data.csv", index=False)
    return True

def UpdateProfile(updated_user):

    updated = updated_user
    # updated.to_csv("random_user_profiles_data.csv", index=False)
    user_profiles.update(worksheet="user_profile", data=updated)
    st.cache_data.clear()
    return True

def UpdateBusiness(updated_business):
    
    updatd = updated_business
    # updatd.to_csv("business_df_after_more_clean.csv", index=False)
    business_data.update(worksheet="business", data=updatd)    
    return True


def DeleteProfile(email):

    df = user_profiles.read(worksheet="user_profile")
    df = df[df['Email'] != email]
    # df.to_csv("random_user_profiles_data.csv", index=False)

    user_profiles.update(worksheet="user_profile", data=df)
    
    st.cache_data.clear()
    
    return True
    