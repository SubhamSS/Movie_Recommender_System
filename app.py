import streamlit as st
from PIL import Image
import pickle
import pandas as pd
import requests

st.title("Movie Recommender System")

def fetch_poster(movie_id): #Get movie poster from tmdb
    try:
        # try to load the poster
        response = requests.get(
            'https://api.themoviedb.org/3/movie/{}?api_key=be347e479b6509b56fa0c9ac54ce5116'.format(movie_id))
        data = response.json()
        return "https://image.tmdb.org/t/p/w342/" + data['poster_path']
    except KeyError:
        return("no_poster.jpg")
        # if a "KeyError" was raised, no poster

def recommend(movie): #Get recommendations basis the similarity matrix
    index = movies[movies['title'] == "Se7en"].index[0]
    distances = similarity[index]
    mov_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in mov_list:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names,recommended_movie_posters

with open('movies_dict.pkl','rb') as f:
    movies_list = pickle.load(f)
#movies_list = pickle.load('movies_dict.pkl','rb')
movies = pd.DataFrame(movies_list)

with open('similarity.pkl','rb') as f:
    similarity = pickle.load(f)

#dropdown for user movie selection
selected_movie = st.selectbox('Select your movie',movies['title'].values)

#recommend basis user selection
if(st.button('Recommend')):
    reco_name, reco_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(reco_name[0])
        st.image(reco_posters[0])
    with col2:
        st.text(reco_name[1])
        st.image(reco_posters[1])
    with col3:
        st.text(reco_name[2])
        st.image(reco_posters[2])
    with col4:
        st.text(reco_name[3])
        st.image(reco_posters[3])
    with col5:
        st.text(reco_name[4])
        st.image(reco_posters[4])

    col6, col7, col8, col9, col10 = st.columns(5)
    with col6:
        st.text(reco_name[5])
        st.image(reco_posters[5])
    with col7:
        st.text(reco_name[6])
        st.image(reco_posters[6])
    with col8:
        st.text(reco_name[7])
        st.image(reco_posters[7])
    with col9:
        st.text(reco_name[8])
        st.image(reco_posters[8])
    with col10:
        st.text(reco_name[9])
        st.image(reco_posters[9])



