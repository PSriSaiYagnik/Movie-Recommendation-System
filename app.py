import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    try:
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=0b899975abbf399f2fbe3965c7bfbe76&language=en-US')
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching poster: {e}")
        return None

def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_movies_posters = []
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies.append(movies.iloc[i[0]].title)
            poster_url = fetch_poster(movie_id)
            if poster_url:
                recommended_movies_posters.append(poster_url)
            else:
                recommended_movies_posters.append("https://via.placeholder.com/500x750?text=No+Poster+Available")
        return recommended_movies, recommended_movies_posters
    except IndexError:
        st.error("Movie not found in the database.")
        return [], []

# Load movie data and similarity matrix
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app
st.title('Movie Recommendation System')

selected_movie_name = st.selectbox(
    "Select a movie to get recommendations",
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    if names and posters:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(names[0])
            st.image(posters[0])
        with col2:
            st.text(names[1])
            st.image(posters[1])
        with col3:
            st.text(names[2])
            st.image(posters[2])
        with col4:
            st.text(names[3])
            st.image(posters[3])
        with col5:
            st.text(names[4])
            st.image(posters[4])
    else:
        st.warning("No recommendations available.")