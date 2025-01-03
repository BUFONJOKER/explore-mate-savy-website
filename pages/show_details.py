import streamlit as st
import folium

from streamlit_folium import st_folium

import pandas as pd 
import ast
# import the BusinessDataFrame function from data_frame.py
from data_frame import BusinessDataFrame,ReviewsDataFrame, UsersDataFrame, UserProfiles, UpdateProfile

df = BusinessDataFrame()
df_reviews = ReviewsDataFrame()
df_users = UsersDataFrame()
df_user_profiles = UserProfiles()

# Create two columns for layout
left_column, right_column = st.columns([20, 5])




if not st.query_params:
    st.title("Show Details Page")

else:
    # get the business_id from the query parameters
    business_id = st.query_params["business_id"]
    email = None
    if "email" in st.query_params:
        email = st.query_params["email"]
    
    if email:
       
        visited = df_user_profiles[df_user_profiles['Email'] == email]['VisitedPlaces'].astype(str).values[0]
                
            # Check if 'VisitedPlaces' is NaN or empty
        if visited == "nan" : 
            df_user_profiles.loc[df_user_profiles['Email'] == email, 'VisitedPlaces'] = business_id
        else:
                    # If there are already visited places, append the new business_id
            df_user_profiles.loc[df_user_profiles['Email'] == email, 'VisitedPlaces'] = visited + "," + business_id
                
        update = UpdateProfile(df_user_profiles)
         
        st.query_params.email = email

        with right_column:
            profile_button = st.link_button("👤 Profile", f"/user_detail?email={email}")
            logout_button = st.button(" Logout",icon=":material/logout:")

            if logout_button:
                st.session_state.clear()
                del st.query_params.email
                st.switch_page("business_discovery.py")

    # filter the rows based on the business_id
    business = df[df['business_id'] == business_id]

    # get the values from the filtered row
    name = business['name'].values[0]
    address = business['address'].values[0]
    city = business['city'].values[0]
    state = business['state'].values[0]
    postal_code = business['postal_code'].values[0]
    stars = int(business['stars'].values[0])
    review_count = business['review_count'].values[0]
    is_open = business['is_open'].values[0]
    longitude = business['longitude'].values[0]
    latitude = business['latitude'].values[0]
    attributes = business['attributes'].values[0]
    attributes_dict = ast.literal_eval(attributes)

    categories = business['categories'].values[0]

    hours = business['hours'].values[0]
    # change the hours string to a dictionary
    operation_hours = ast.literal_eval(hours)



    with left_column:
        st.title(f"Business Details")

        # Function to display the stars
        def display_stars(star_rating):
            # Define the total number of stars (e.g., 5)
            total_stars = 5
            # Calculate the filled stars and empty stars
            filled_stars = "⭐" * star_rating
            empty_stars = "☆" * (total_stars - star_rating)
            # Combine the filled and empty stars
            return filled_stars + empty_stars

        st.header(f"Name : {name}")
        st.header(f"**Ratings:** {display_stars(stars)}")
        st.header("Address")
        st.write(address+", "+city+", "+state+", "+str(postal_code))

        if is_open == 1:
            st.header("Business is Open")
        elif is_open == 0:
            st.header("Business is Closed")
            
        st.header("Categories")
        st.write(categories)    


        # create a list of strings for the attributes
        attribute_list = [f"**{key}**: {value}" for key, value in attributes_dict.items()]
        st.header("Attributes")
        for i in attribute_list:
            st.write(i)    
            
        # Create a list of strings with day and hours combined
        day_hour_list = [f"{day}: {hours}" for day, hours in operation_hours.items()]
        st.header("Operation Hours")

        for i in day_hour_list:
            st.write(i)


        # Filter the reviews for the given business_id
        filtered_reviews = df_reviews[df_reviews['business_id'] == business_id][['user_id','text']].head(5)




        # Display the filtered users and their reviews
        st.header("Reviews for the Business")


            
        if(filtered_reviews.empty):
            st.write("No reviews found.")
        for i in range(len(filtered_reviews)):
            st.header(f"Review By **{df_users['name'].iloc[i]}**")
            st.write(filtered_reviews['text'].iloc[i])
            
            
        if email:
            st.header("If you liked this place press like")
            like_button = st.button("Like", icon="👍")
            if like_button:
                st.success("You Liked this place")
                
                # Retrieve the 'LikedPlaces' column for the user
                liked = df_user_profiles[df_user_profiles['Email'] == email]['LikedPlaces'].values[0]
                
                # Check if 'LikedPlaces' is NaN or empty
                if pd.isna(liked) or liked == "":  # Checking for NaN or empty string
                    # If no liked places yet, add the business_id
                    df_user_profiles.loc[df_user_profiles['Email'] == email, 'LikedPlaces'] = str(business_id)
                else:
                    # If there are already liked places, append the new business_id
                    df_user_profiles.loc[df_user_profiles['Email'] == email, 'LikedPlaces'] = liked + "," + str(business_id)

                # After updating, call the UpdateProfile function to persist changes (if required)
                update = UpdateProfile(df_user_profiles)



        st.header("Business Location")
        google_maps_url = f"https://www.google.com/maps?q={latitude},{longitude}&hl=en"

        # Display the link with a location symbol (using the map emoji)
        st.link_button(url=google_maps_url, icon=":material/location_searching:", label="View on Google Maps")


        # Create a Folium map centered at the business location with a specified zoom level
        m = folium.Map(location=[latitude, longitude], zoom_start=15)

        # Add a marker for the business location
        marker = folium.Marker([latitude, longitude], popup='Business Location')
        # Open the popup automatically
        marker.add_child(folium.Popup('Business Location', parse_html=True)).add_to(m)

        # Render the map in Streamlit
        st_folium(m)

