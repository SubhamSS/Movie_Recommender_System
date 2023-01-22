import numpy
import openpyxl
import pandas as pd
from tags_functions import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer
import pickle

def prepn():

    # load dataset from different csv files and create single dataframe
    dirname = 'C:/Personal_Data/recom_data/movies_2/' #CHANGE AS PER REQUIREMENT
    credits = pd.read_csv(dirname+'credits.csv')
    keywords = pd.read_csv(dirname + 'keywords.csv')
    metadata = pd.read_csv(dirname + 'movies_metadata.csv')

    metadata['id'] = pd.to_numeric(metadata['id'], errors ='coerce')
    metadata = metadata[metadata['id'].notna()]

    metadata['id'] = metadata['id'].astype(int)

    movies = metadata.merge(credits, on='id')
    movies = movies.merge(keywords, on='id')
    movies = movies[movies['title'].notna()]

    movies = movies[movies['status']=="Released"]
    movies = movies[movies['vote_count']>=10]

    #SELECT RELEVANT FEATURES
    movies = movies[['cast','crew','id','keywords','adult','belongs_to_collection',
                     'genres','overview','popularity','production_companies',
                     'release_date','runtime','tagline','title','vote_count','vote_average']]

    nas = movies.isna().sum()

    #DROP DUPLICATES
    movies = movies.drop_duplicates()
    movies = movies.drop_duplicates(subset='id', keep='first')

    #extraction of various features of the movie
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

    #remove_space
    movies['director'] = movies['director'].apply(remove_space)
    movies['producer'] = movies['producer'].apply(remove_space)
    movies['music_composer'] = movies['music_composer'].apply(remove_space)
    movies['screenplay'] = movies['screenplay'].apply(remove_space)
    movies['writer'] = movies['writer'].apply(remove_space)
    movies['cast'] = movies['cast'].apply(remove_space)
    movies['genres'] = movies['genres'].apply(remove_space)
    movies['keywords'] = movies['keywords'].apply(remove_space)
    movies['belongs_to_collection'] = movies['belongs_to_collection'].apply(remove_space)
    movies['production_companies'] = movies['production_companies'].apply(remove_space)

    movies['overview'] = movies['overview'].astype(str)
    movies['overview'] = movies['overview'].apply(lambda x: x.split())

    #create tags
    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + \
                     movies['cast'] + movies['director'] + movies['producer'] + movies['writer'] + \
                     movies['music_composer'] + movies['screenplay'] + movies['belongs_to_collection'] + \
                     movies['production_companies']

    mov_feat = movies.drop(columns=['overview','genres','keywords','cast','crew',
                                    'production_companies','belongs_to_collection',
                                    'director','producer','writer','screenplay','music_composer'])

    #join all tags
    mov_feat['tags'] = mov_feat['tags'].apply(lambda x: " ".join(x))
    mov_feat['tags'] = mov_feat['tags'].apply(lambda x: x.lower())

    #convert to root word
    mov_feat['tags'] = mov_feat['tags'].apply(stem)

    mov_feat.reset_index(drop=True, inplace=True)

    #get top 5000 words excluding english stop words
    cv = CountVectorizer(max_features=5000, stop_words='english')

    #cosine similarity to determine similarity between 2 movies
    vector = cv.fit_transform(mov_feat['tags']).toarray()
    similarity = cosine_similarity(vector)

    def recommend(movie):
        index = mov_feat[mov_feat['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        for i in distances[1:10]:
            print(mov_feat.iloc[i[0]].title)

    recommend("Se7en")
    #store the similarity data and feature extracted data
    #pickle.dump(mov_feat.to_dict(), open('movies_dict.pkl','wb'))
    #pickle.dump(similarity, open('similarity.pkl', 'wb'))


if __name__ == '__main__':
    prepn()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
