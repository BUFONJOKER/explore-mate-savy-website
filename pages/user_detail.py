import streamlit as st
from data_frame import UserProfiles, BusinessDataFrame, DeleteProfile

with st.container():

    df = UserProfiles()

    df_business = BusinessDataFrame()
    df['VisitedPlaces'] = df['VisitedPlaces'].astype(str)
    df['LikedPlaces'] = df['LikedPlaces'].astype(str)
    if 'email' not in st.query_params:
        st.write("Please login to view your profile")
        login_button = st.button("Login")
        if login_button:
            st.switch_page("pages/login.py")
        st.stop()
        
            
    email = st.query_params.email
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        if email:
            st.session_state.email = email
            home_button = st.button("🏠 Home")
            if home_button:
                st.switch_page("business_discovery.py")
            
    with col2:
        update = st.button("Update Profile", icon=":material/edit:")
        if update:
            st.session_state.email = email
            if "email" in st.session_state:
                st.switch_page("pages/update_user.py")
    with col3:
        # delete button
        delete = st.button("Delete")
        if delete:
            if email in df['Email'].values:
                delete_profile = DeleteProfile(email)
                if delete_profile:
                    st.success("Profile Deleted Successfully")
                    st.session_state.clear()
                    del st.query_params.email
                    st.switch_page("business_discovery.py")
    
    with col4:
        logout_button = st.button(" Logout",icon=":material/logout:")

        if logout_button:
            st.session_state.clear()
            del st.query_params.email
            st.switch_page("business_discovery.py")
    
    first_name = df[df['Email'] == email]['FirstName'].values[0]
    last_name = df[df['Email'] == email]['LastName'].values[0]
   
    
    visited_places = df[df['Email'] == email]['VisitedPlaces'].values[0]
    list_visited = visited_places.split(",")    
    
    liked_places = df[df['Email'] == email]['LikedPlaces'].values[0]
    list_likes = liked_places.split(",")

    st.title(f"{first_name} {last_name} Details")
    
    st.header("Email")
    st.write(email)

    

    # make dataframe with the business details where business_id is in the liked_places
    
    df_liked_places = df_business[df_business['business_id'].isin(list_likes)]
    
    df_visited_places = df_business[df_business['business_id'].isin(list_visited)]


    def display_stars(star_rating):
            # Define the total number of stars (e.g., 5)
            total_stars = 5
                # Calculate the filled stars and empty stars
            filled_stars = "⭐" * star_rating
            empty_stars = "☆" * (total_stars - star_rating)
                # Combine the filled and empty stars
            return filled_stars + empty_stars
        
    if list_likes[0]!="nan":
        
        st.header("----------Liked Places----------")
        for index, row in df_liked_places.iterrows():
            stars = row['stars']
            stars_display = display_stars(int(stars))
            st.header(f"{row['name']} - {stars_display}")    
            st.write(f"Address: {row['address']} {row['city']} {row['state']} {row['postal_code']}")
            st.write(f"Categories: {row['categories']}")
            st.link_button("💁 Check details", f"/show_details?business_id={row['business_id']}&email={email}")

    if list_visited[0]!="nan":
        st.header("----------Visited Places----------")
        for index, row in df_visited_places.iterrows():
            stars = row['stars']
            stars_display = display_stars(int(stars))
            st.header(f"{row['name']} - {stars_display}")    
            st.write(f"Address: {row['address']} {row['city']} {row['state']} {row['postal_code']}")
            st.write(f"Categories: {row['categories']}")
            st.link_button("💁 Check details", f"/show_details?business_id={row['business_id']}&email={email}")


