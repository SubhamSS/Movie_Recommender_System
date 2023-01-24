#run this code to get the recommend.pkl and movies_dict.pkl file
# Rows 102 to 108 can be removed, this is just to test if the algorithm works properly

import numpy
import openpyxl
import pandas as pd
from tags_functions import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import sklearn.preprocessing as preprocess

def prepn():

    # load dataset from different csv files and create single dataframe
    dirname = 'C:/Personal_Data/recom_data/movies_2/' #CHANGE AS PER REQUIREMENT
    credits = pd.read_csv(dirname + 'credits.csv')
    keywords = pd.read_csv(dirname + 'keywords.csv')
    metadata = pd.read_csv(dirname + 'movies_metadata.csv')
    print("csvs loaded")

    metadata['id'] = pd.to_numeric(metadata['id'], errors ='coerce')
    metadata = metadata[metadata['id'].notna()]

    metadata['id'] = metadata['id'].astype(int)

    movies = metadata.merge(credits, on='id')
    movies = movies.merge(keywords, on='id')
    movies = movies[movies['title'].notna()]
    movies = movies[movies['release_date'].notna()]

    movies = movies[movies['status']=="Released"]
    movies = movies[movies['vote_count']>=10]#optional, delete line to feature all movies
    print("merged")

    #SELECT RELEVANT FEATURES
    movies = movies[['cast','crew','id','keywords','adult','belongs_to_collection',
                     'genres','overview','popularity','production_companies',
                     'release_date','runtime','tagline','title','vote_count','vote_average']]

    nas = movies.isna().sum()

    #DROP DUPLICATES
    movies = movies.drop_duplicates()
    movies = movies.drop_duplicates(subset='id', keep='first')

    #extraction of various features of the movie
    movies['release_date'] = movies['release_date'].apply(fetch_year)
    movies["title"] = movies['title'].astype(str) +" ("+ movies["release_date"].astype(str)+")"

    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)
    movies['belongs_to_collection'] = movies['belongs_to_collection'].apply(convertfromdict)
    movies['production_companies'] = movies['production_companies'].apply(convert)

    movies['cast'] = movies['cast'].apply(convert)
    movies['cast'] = movies['cast'].apply(lambda x: x[0:5])

    movies['director'] = movies['crew'].apply(fetch_director)
    movies['producer'] = movies['crew'].apply(producer)
    movies['music_composer'] = movies['crew'].apply(fetch_music_composer)
    movies['screenplay'] = movies['crew'].apply(screenplay)
    movies['writer'] = movies['crew'].apply(writer)
    movies['pop_rating'] = movies['vote_count']*movies['vote_average']

    print("feature extraction done")

    #Normalization of numerics
    scaler = preprocess.MinMaxScaler(feature_range=(0, 1))

    temp = movies[['pop_rating','vote_average','popularity']].to_numpy()
    temp_sc = scaler.fit_transform(temp)
    movies['sc_pop_rating'] = temp_sc[:,0].tolist()
    movies['sc_vot_avg'] = temp_sc[:,1].tolist()
    movies['sc_pol'] = temp_sc[:,2].tolist()
    print("normalization done")

    #remove_space
    movies['director'] = movies['director'].apply(remove_space)
    movies['producer'] = movies['producer'].apply(remove_space)
    movies['music_composer'] = movies['music_composer'].apply(remove_space)
    movies['screenplay'] = movies['screenplay'].apply(remove_space)
    movies['writer'] = movies['writer'].apply(remove_space)
    movies['cast'] = movies['cast'].apply(remove_space)

    movies['keywords'] = movies['keywords'].apply(remove_space)
    movies['belongs_to_collection'] = movies['belongs_to_collection'].apply(remove_space)
    movies['production_companies'] = movies['production_companies'].apply(remove_space)

    movies['overview2'] = movies['overview'].astype(str)
    movies['overview2'] = movies['overview2'].apply(lambda x: x.split())
    print("space removed")

    #create tags
    movies['tags'] = movies['overview2'] + movies['keywords'] + movies['director'] +\
                     movies['producer'] + movies['writer'] + \
                     movies['music_composer'] + movies['screenplay'] + \
                     movies['production_companies'] \
                     #+ movies['genres'] + movies['cast'] + movies['belongs_to_collection']

    mov_feat = movies.drop(columns=['keywords','crew','adult','popularity', 'overview2',
                                    'production_companies','music_composer','pop_rating',
                                    'director','producer','writer','screenplay',
                                    'runtime','tagline','vote_count','vote_average'])

    mov_feat.reset_index(drop=True, inplace=True)
    print("tags created")
    lll=0

    #TAGS SIMILARITY
    #join all tags
    mov_feat['tags'] = mov_feat['tags'].apply(lambda x: " ".join(x))
    mov_feat['tags'] = mov_feat['tags'].apply(lambda x: x.lower())

    #convert to root word
    mov_feat['tags'] = mov_feat['tags'].apply(stem)

    #get top 5000 words excluding english stop words
    cv_tag = CountVectorizer(max_features=5000, stop_words='english')

    #cosine similarity to determine similarity between 2 movies
    vector_tag = cv_tag.fit_transform(mov_feat['tags']).toarray()
    tags_sim = cosine_similarity(vector_tag)
    print("tags similarity")

    # COLLECTION
    # get top
    mov_feat['belongs_to_collection'] = mov_feat['belongs_to_collection'].apply(lambda x: " ".join(x))
    mov_feat['belongs_to_collection'] = mov_feat['belongs_to_collection'].apply(lambda x: x.lower())
    cv_coll = CountVectorizer(max_features=200)

    # cosine similarity to determine similarity between 2 movies
    vector_coll = cv_coll.fit_transform(mov_feat['belongs_to_collection']).toarray()
    tags_sim = tags_sim + 0.2*cosine_similarity(vector_coll)
    print("collection similarity done")

    #GENRES
    # join all
    mov_feat['genres2'] = mov_feat['genres'].apply(remove_space)
    mov_feat['genres2'] = mov_feat['genres2'].apply(lambda x: " ".join(x))
    mov_feat['genres2'] = mov_feat['genres2'].apply(lambda x: x.lower())

    # convert to root word
    mov_feat['genres2'] = mov_feat['genres2'].apply(stem)

    # get top 20 genres
    cv_genre = CountVectorizer(max_features=20, stop_words='english')

    # cosine similarity to determine similarity between 2 movies' genres
    vector_genre = cv_genre.fit_transform(mov_feat['genres2']).toarray()
    tags_sim = tags_sim + 0.05*cosine_similarity(vector_genre)
    print("genres similarity")

    # CAST
    # join all
    mov_feat['cast'] = mov_feat['cast'].apply(lambda x: " ".join(x))
    mov_feat['cast'] = mov_feat['cast'].apply(lambda x: x.lower())

    # get top 200 popular actors
    cv_cast = CountVectorizer(max_features=200)

    # cosine similarity to determine similarity between 2 movies'
    vector_cast = cv_cast.fit_transform(mov_feat['cast']).toarray()
    tags_sim = tags_sim + 0.05*cosine_similarity(vector_cast)
    print("cast similarity")

    #corr_weights = numpy.empty([mov_feat.shape[0], mov_feat.shape[0]], dtype=float)
    for i in range(mov_feat.shape[0]):
        for j in range(mov_feat.shape[0]):
            tags_sim[i][j] = tags_sim[i][j] + 0.08*(1 - abs(mov_feat['sc_pop_rating'][i] - mov_feat['sc_pop_rating'][j])) + \
                                    0.03*(1 - abs(mov_feat['sc_vot_avg'][i] - mov_feat['sc_vot_avg'][j])) + \
                                    0.01*(1 - abs(mov_feat['sc_pol'][i] - mov_feat['sc_pol'][j])) + \
                                    0.04*(1 - abs((mov_feat['release_date'][i] - mov_feat['release_date'][j])/150))
        if(i%10) == 0:
            print("rows completed is {}".format(i))

    print("similarity done")
    #tags_add = tags_sim + corr_weights
    indices = numpy.argsort(tags_sim, axis=-1)
    ind2 = indices[:, -11:-1]
    print("top 10 selected")

    def recommend(movie):
        index = mov_feat[mov_feat['title'] == movie].index[0]
        #print(index)
        for i in range(10):
            movie_rec = ind2[index][9-i]
            #print(movie_rec)
            print(mov_feat.iloc[movie_rec].title)

    recommend("Toy Story (1995)")

    #store the similarity data and feature extracted data
    pickle.dump(mov_feat.to_dict(), open('movies_dict.pkl','wb'))
    pickle.dump(ind2, open('recommend.pkl', 'wb'))
    print("wrote pkl files")


if __name__ == '__main__':
    prepn()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
