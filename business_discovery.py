import streamlit as st
# import the BusinessDataFrame function from data_frame.py
from data_frame import BusinessDataFrame,UserProfiles
from recommendation import RecommendationSystem
# business discovery page

if "email" in st.session_state:
    st.query_params.email = st.session_state.email

if "email" in st.query_params:
    st.session_state.email = st.query_params.email

# Create two columns for layout
left_column, right_column = st.columns([20, 5])

with right_column:
        admin_button = st.button("Admin",icon=":material/shield_person:")
        if admin_button:
            st.switch_page("pages/admin.py")

# Check if the user is logged in
if "email" in st.query_params:
    # User is logged in
    user = st.query_params["email"]
    with right_column:
        # Profile and logout buttons
        
        
        if user:
            profile_button = st.link_button("👤 Profile", f"/user_detail?email={user}")
            
        logout_button = st.button(" Logout",icon=":material/logout:")

        if logout_button:
            st.session_state.clear()
            del st.query_params.email
            
            
            st.rerun()
            
    

else:
    # User is not logged in
    with right_column:
        login_button = st.button("Login", icon=":material/login:")
        if login_button:
            st.switch_page("pages/login.py")
    
with left_column:
        st.title("Explore Mate Savy")
        st.header("(business discovery and recommendation system)")
        df_business = BusinessDataFrame()

        # split the categories column and explode the values
        all_categories = df_business['categories'].str.split(',').explode().str.strip()

        categories = all_categories.unique()

        states = df_business['state'].unique()


        first,second = st.columns([10,10])
        # selectbox to select a business type
        
        with first:
            category = st.selectbox(
            "Select a business",
            categories,
            index=None,
            placeholder="Select category"
            )

        # selectbox to select a state
        with second:
            state = st.selectbox(
            "Select a state",
            states,
            index=None,
            placeholder="Select state"
            )

        # get the cities based on the selected state
        cities = df_business[df_business['state'] == state]['city'].unique()

        third,fourth = st.columns([10,10])
        with third:
            city = st.selectbox(
            "Select a city",
            cities,
            index=None,
            placeholder="Select city"
            )

        # select box to select stars
        with fourth:
            stars = st.selectbox(
            "Select stars",
            [1, 2, 3, 4, 5],
            index=None,
            placeholder="Select stars"
            )

        # tax input to enter reviews count 
        # from min to max
        min_reviews = df_business['review_count'].min()
        max_reviews = df_business['review_count'].max()

        # text input to enter reviews count 
        # from min to max


        
        reviews_filter = st.text_input("Enter reviews count between 5 to 7568")

        # search button selection
        selected = False
        

        if not city and not state and not category and not stars and not reviews_filter:
            selected = True
            st.error("Please select a filter.")

            
        search_button = st.button("Search",icon=":material/search:", disabled=selected)
        # check if city and state and category are not empty
        if search_button:
            # Start with a copy of the DataFrame
            filtered_rows = df_business.copy()

            # Apply filters dynamically
            if city:
                filtered_rows = filtered_rows[filtered_rows['city'].str.contains(city, case=False, na=False)]
            
            if state:
                filtered_rows = filtered_rows[filtered_rows['state'].str.contains(state, case=False, na=False)]
            
            if category:
                filtered_rows = filtered_rows[filtered_rows['categories'].str.contains(category, case=False, na=False)]
            
            if stars:
                filtered_rows = filtered_rows[filtered_rows['stars'] == stars]
            
            if reviews_filter:
                reviews_filter = int(reviews_filter)  # Ensure it's an integer
                filtered_rows = filtered_rows[filtered_rows['review_count'] >= reviews_filter]

            # copy the filtered rows to a new dataframe
            filtered_rows = filtered_rows.copy()
            
            # Check if the filtered rows are empty
            if filtered_rows.empty:
                st.header("No businesses found.")
            else:
                
                
                # Add a show_details link
                
                if "email" in st.query_params:
                    filtered_rows['show_details'] = filtered_rows['business_id'].apply(
                    lambda x: f"/show_details?business_id={x}&email={st.query_params.email}"
                )
                elif "email" not in st.query_params:
                    filtered_rows['show_details'] = filtered_rows['business_id'].apply(
                    lambda x: f"/show_details?business_id={x}"
                )

                # Create a new DataFrame for the table
                table_df = filtered_rows[['name', 'city', 'state', 'stars', 'review_count', 'show_details']]

                # Set session state
                st.session_state.key = table_df

                # Display the table
                st.data_editor(
                    table_df,
                    key="table_df",
                    width=1000,
                    column_config={
                        "show_details": st.column_config.LinkColumn(display_text="Show Details"),
                    },
                    hide_index=True,
                )

if "email" not in st.query_params:
    st.error("Please login to view recommendations")

elif "email" in st.query_params:
    
    # User is logged in
    user = st.query_params["email"]
    df_user = UserProfiles()
    user_row = df_user[df_user['Email'] == user]
    
    if user_row['LikedPlaces'].astype(str).values[0] == "nan" and user_row['VisitedPlaces'].astype(str).values[0] == "nan":
            st.header("Please visit or like some places to get recommendations")
    else:
            recommendations = RecommendationSystem(user)
            
            if recommendations:
                recommended_data = df_business[df_business['business_id'].isin(recommendations)]
                   
                # Function to display the stars
                def display_stars(star_rating):
                    # Define the total number of stars (e.g., 5)
                    total_stars = 5
                        # Calculate the filled stars and empty stars
                    filled_stars = "⭐" * star_rating
                    empty_stars = "☆" * (total_stars - star_rating)
                        # Combine the filled and empty stars
                    return filled_stars + empty_stars
                
                
                for index, row in recommended_data.iterrows():
                    stars = row['stars']
                    stars_display = display_stars(int(stars))
                    st.header(f"Name: {row['name']} - {stars_display}")    
                    st.write(f"Address: {row['address']} {row['city']} {row['state']} {row['postal_code']}")
                    st.write(f"Categories: {row['categories']}")
                    
                    st.link_button("💁 Check details", f"/show_details?business_id={row['business_id']}&email={user}")
            else:
                st.error("No recommendations available")