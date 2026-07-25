import streamlit as st
import pickle
import requests
import os
import gdown

API_KEY = st.secrets["TMDB_API_KEY"]

# Load data
# Load movies
movies = pickle.load(open("movies.pkl", "rb"))

# Download similarity.pkl if it doesn't exist
if not os.path.exists("similarity.pkl"):
    st.info("Downloading recommendation model... Please wait.")

    file_id = "13NH_5FFuJQCPFr0KpbWB1dnnP5IptioZ"
    url = f"https://drive.google.com/uc?id={file_id}"

    gdown.download(url, "similarity.pkl", quiet=False)

# Load similarity matrix
similarity = pickle.load(open("similarity.pkl", "rb"))

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=15)

    data = response.json()

    poster_path = data.get("poster_path")

    if poster_path:
        return "https://image.tmdb.org/t/p/w500" + poster_path

    return "https://via.placeholder.com/500x750?text=No+Poster"

# Recommendation Function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        movie_title = movies.iloc[i[0]].title

        print(f"Fetching: {movie_title} | ID: {movie_id}")

        try:
            poster = fetch_poster(movie_id)
        except Exception as e:
            print("ERROR:", e)
            poster = "https://via.placeholder.com/500x750?text=No+Poster"

        recommended_movies.append(movie_title)
        recommended_posters.append(poster)

    return recommended_movies, recommended_posters

# Website Title
st.title("🎬 Movie Recommendation System")

# Dropdown
movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Select a Movie",
    movie_list
)

# Button
if st.button("Recommend"):

    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(recommended_movie_posters[0])
        st.write(recommended_movie_names[0])

    with col2:
        st.image(recommended_movie_posters[1])
        st.write(recommended_movie_names[1])

    with col3:
        st.image(recommended_movie_posters[2])
        st.write(recommended_movie_names[2])

    with col4:
        st.image(recommended_movie_posters[3])
        st.write(recommended_movie_names[3])

    with col5:
        st.image(recommended_movie_posters[4])
        st.write(recommended_movie_names[4])