import streamlit as st
from PIL import Image
import pickle
import pandas as pd
import requests
import ast
import base64

def add_bg_from_local(image_file): #load background, put image_file in same folder as app.py
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
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

def fetch_overview(movie): #Get movie overview
        index = movies[movies['title'] == movie].index[0]
        return movies.iloc[index].overview

def fetch_genres(movie):  # Get movie overview
    index = movies[movies['title'] == movie].index[0]
    lst = movies.iloc[index].genres
    resultString = ','.join(lst)
    return resultString

def recommend(movie):  #Get the recommended movies from the pkl files
    index = movies[movies['title'] == movie].index[0]
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in range(10):
        movie_rec = similarity[index][9-i]
        movie_id = movies.iloc[movie_rec].id
        recommended_movie_names.append(movies.iloc[movie_rec].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters


with open('movies_dict.pkl','rb') as f:
    movies_list = pickle.load(f)
movies = pd.DataFrame(movies_list)

with open('recommend.pkl','rb') as f:
    similarity = pickle.load(f)


add_bg_from_local('blue_bg.jpg') #load background
st.markdown(f'<h1 style="color:#f1f0eb;font-size:40px;">Movie Recommender System</h1>', unsafe_allow_html=True)

selected_movie = st.selectbox("Select Movie", movies['title'].values) #dropdown for user movie selection
sel_id = movies[movies['title'] == selected_movie].index[0]
ind_id = movies.iloc[sel_id].id
mov_img = fetch_poster(ind_id)
mov_ovr = fetch_overview(selected_movie)
mov_gen = fetch_genres(selected_movie)

colh1, mid, colh2 = st.columns([20,1,20])
with colh1:
    st.image(mov_img, width=300)
with colh2:
    st.markdown(f'<h1 style="color:#33ff33;font-size:30px;">{selected_movie}</h1>', unsafe_allow_html=True)

    html_mov = f"""
        <style>
        p.a {{
          font: 20px Calibri;
        }}
        </style>
        <span style="color:white">
        <p class="a">Genres: {mov_gen}</p>
        <p class="a">{mov_ovr}</p>
        </span>
        """
    st.markdown(html_mov, unsafe_allow_html=True)

#recommend 10 movies basis user selection
if(st.button('Recommend')):
    reco_name, reco_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(reco_posters[0])
        st.caption(f'<center><text style="color:#33ff33;font-size:12px;font-family: Verdana;'
                   f'">{reco_name[0]}</text></center>', unsafe_allow_html=True)
    with col2:
        st.image(reco_posters[1])
        st.caption(f'<center><text style="color:#33ff33;font-size:12px;font-family: Verdana;'
                   f'">{reco_name[1]}</text></center>', unsafe_allow_html=True)
    with col3:
        st.image(reco_posters[2])
        st.caption(f'<center><text style="color:#33ff33;font-size:12px;font-family: Verdana;'
                   f'">{reco_name[2]}</text></center>', unsafe_allow_html=True)
    with col4:
        st.image(reco_posters[3])
        st.caption(f'<center><text style="color:#33ff33;font-size:12px;font-family: Verdana;'
                   f'">{reco_name[3]}</text></center>', unsafe_allow_html=True)
    with col5:
        st.image(reco_posters[4])
        st.caption(f'<center><text style="color:#33ff33;font-size:12px;font-family: Verdana;'
                   f'">{reco_name[4]}</text></center>', unsafe_allow_html=True)

    st.markdown(f'<br>', unsafe_allow_html=True)

    col6, col7, col8, col9, col10 = st.columns(5)
    with col6:
        st.image(reco_posters[5])
        st.caption(f'<center><text style="color:#33ff33;font-size:12px;font-family: Verdana;'
                   f'">{reco_name[5]}</text></center>', unsafe_allow_html=True)
    with col7:
        st.image(reco_posters[6])
        st.caption(f'<center><text style="color:#33ff33;font-size:12px;font-family: Verdana;'
                   f'">{reco_name[6]}</text></center>', unsafe_allow_html=True)
    with col8:
        st.image(reco_posters[7])
        st.caption(f'<center><text style="color:#33ff33;font-size:12px;font-family: Verdana;'
                   f'">{reco_name[7]}</text></center>', unsafe_allow_html=True)
    with col9:
        st.image(reco_posters[8])
        st.caption(f'<center><text style="color:#33ff33;font-size:12px;font-family: Verdana;'
                   f'">{reco_name[8]}</text></center>', unsafe_allow_html=True)
    with col10:
        st.image(reco_posters[9])
        st.caption(f'<center><text style="color:#33ff33;font-size:12px;font-family: Verdana;'
                   f'">{reco_name[9]}</text></center>', unsafe_allow_html=True)



