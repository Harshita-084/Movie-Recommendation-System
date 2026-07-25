import streamlit as st
import pickle
import requests
import os
import gdown

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

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

def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    for attempt in range(3):  # Retry up to 3 times
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()

            data = response.json()

            poster = (
                "https://image.tmdb.org/t/p/w500" + data["poster_path"]
                if data.get("poster_path")
                else "https://via.placeholder.com/500x750?text=No+Poster"
            )

            rating = data.get("vote_average", "N/A")
            release_date = data.get("release_date", "")
            year = release_date[:4] if release_date else "N/A"

            return poster, rating, year

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed for movie {movie_id}: {e}")

    return (
        "https://via.placeholder.com/500x750?text=No+Poster",
        "N/A",
        "N/A",
    )

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
    recommended_ratings = []
    recommended_years = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        movie_title = movies.iloc[i[0]].title

        print(f"Fetching: {movie_title} | ID: {movie_id}")

        try:
            poster, rating, year = fetch_movie_details(movie_id)
        except Exception as e:
            print("ERROR:", e)
            poster = "https://via.placeholder.com/500x750?text=No+Poster"

        recommended_movies.append(movie_title)
        recommended_posters.append(poster)
        recommended_ratings.append(rating)
        recommended_years.append(year)

    return (
        recommended_movies,
        recommended_posters,
        recommended_ratings,
        recommended_years
)

# Website Title
st.title("🎬 Movie Recommendation System")

st.markdown(
    """
    Discover movies similar to your favorite films using a
    **Content-Based Recommendation System** powered by Machine Learning.
    """
)

st.divider()

with st.sidebar:
    st.header("About")

    st.write(
        """
        This application recommends movies based on content similarity.

        **Technologies Used**
        - Python
        - Pandas
        - Scikit-learn
        - NLTK
        - Streamlit
        - TMDB API
        """
    )

    st.divider()

    st.success("Project by Harshita")

# Dropdown
movie_list = movies['title'].values

selected_movie = st.selectbox(
    "🎥 Choose your favorite movie",
    movie_list
)

# Button
if st.button("🍿 Get Recommendations"):

    with st.spinner("Finding similar movies..."):

        (
            recommended_movie_names,
            recommended_movie_posters,
            recommended_movie_ratings,
            recommended_movie_years,
        ) = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(recommended_movie_posters[0], use_container_width=True)

        st.markdown(f"**{recommended_movie_names[0]}**")

        st.write(f"⭐ Rating: {recommended_movie_ratings[0]}")

        st.write(f"📅 Year: {recommended_movie_years[0]}")

    with col2:
        st.image(recommended_movie_posters[1], use_container_width=True)

        st.markdown(f"**{recommended_movie_names[1]}**")

        st.write(f"⭐ Rating: {recommended_movie_ratings[1]}")

        st.write(f"📅 Year: {recommended_movie_years[1]}")
    with col3:
       st.image(recommended_movie_posters[2], use_container_width=True)

       st.markdown(f"**{recommended_movie_names[2]}**")

       st.write(f"⭐ Rating: {recommended_movie_ratings[2]}")

       st.write(f"📅 Year: {recommended_movie_years[2]}")

    with col4:
       st.image(recommended_movie_posters[3], use_container_width=True)

       st.markdown(f"**{recommended_movie_names[3]}**")

       st.write(f"⭐ Rating: {recommended_movie_ratings[3]}")

       st.write(f"📅 Year: {recommended_movie_years[3]}")

    with col5:
       st.image(recommended_movie_posters[4], use_container_width=True)

       st.markdown(f"**{recommended_movie_names[4]}**")

       st.write(f"⭐ Rating: {recommended_movie_ratings[4]}")

       st.write(f"📅 Year: {recommended_movie_years[4]}")

       st.divider()

st.markdown(
    """
    <div style="text-align: center; color: gray;">
        Built with ❤️ using Python, Streamlit, Scikit-learn & TMDB API
    </div>
    """,
    unsafe_allow_html=True
)