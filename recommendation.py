import streamlit as st
import pandas as pd
from data_frame import UserProfiles
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def RecommendationSystem(email_for_recommendation):
    df = UserProfiles()
    
    # Fill missing values in 'VisitedPlaces' and 'LikedPlaces' with empty strings
    df["VisitedPlaces"] = df["VisitedPlaces"].fillna("")
    df["LikedPlaces"] = df["LikedPlaces"].fillna("")
    
    user = df[df["Email"] == email_for_recommendation].iloc[0]
    if not user['LikedPlaces']:
        df["Interactions"] = df["VisitedPlaces"]
        st.header("Recommendations using Visited Places")
    
    else:
        df["Interactions"] = df["VisitedPlaces"] + "," + df["LikedPlaces"]
        st.header("Recommendations using Visited and liked places")
    # Step 1: Convert interactions into numerical vectors using CountVectorizer
    vectorizer = CountVectorizer(tokenizer=lambda x: x.split(","), token_pattern=None)  # Explicitly set token_pattern to None
    interaction_matrix = vectorizer.fit_transform(df["Interactions"])

    # Step 2: Compute pairwise cosine similarity
    similarity_matrix = cosine_similarity(interaction_matrix)

    # Convert similarity matrix to a DataFrame for easy understanding
    similarity_df = pd.DataFrame(similarity_matrix, index=df["Email"], columns=df["Email"])

    # Step 3: Recommendation Function
    def recommend_places(user_email, top_n=3):
        if user_email not in similarity_df.index:
            return f"User {user_email} not found!"
        
        # Retrieve the user data
        user_row = df[df["Email"] == user_email].iloc[0]
        
        # If user has liked places, use liked places, otherwise use visited places
        target_user_places = set()
        
        if user_row["LikedPlaces"]:
            target_user_places = set(user_row["LikedPlaces"].split(","))
        elif user_row["VisitedPlaces"]:
            target_user_places = set(user_row["VisitedPlaces"].split(","))
        else:
            return "No interactions available for this user. Please visit or like places to receive recommendations."

        # Get the similarity scores for the target user
        user_similarities = similarity_df[user_email].sort_values(ascending=False)
        
        # Exclude the user themselves
        user_similarities = user_similarities[user_similarities.index != user_email]
        
        # Find similar users
        similar_users = user_similarities.head(top_n).index
        
        # Collect places liked and visited by similar users but not already interacted by the target user
        recommended_places = set()
        
        for similar_user in similar_users:
            similar_user_row = df[df["Email"] == similar_user].iloc[0]
            
            # Collect places liked by similar users
            if similar_user_row["LikedPlaces"]:
                similar_user_places = set(similar_user_row["LikedPlaces"].split(","))
                recommended_places.update(similar_user_places - target_user_places)

            # Collect places visited by similar users
            if similar_user_row["VisitedPlaces"]:
                similar_user_visited_places = set(similar_user_row["VisitedPlaces"].split(","))
                recommended_places.update(similar_user_visited_places - target_user_places)
        
        return list(recommended_places) if recommended_places else False

    # Generate recommendations for the provided email
    recommendations = recommend_places(email_for_recommendation, top_n=2)
    
    return recommendations


