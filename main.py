
import numpy
import openpyxl
import pandas as pd
from tags_functions import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def prepn():
    # load dataset from dat file
    dirname = 'C:/Personal_Data/Reco_system_py/movies_2/'
    credits = pd.read_csv(dirname+'credits.csv')
    keywords = pd.read_csv(dirname + 'keywords.csv')
    metadata = pd.read_csv(dirname + 'movies_metadata.csv')

    nan_values = metadata[metadata.isna().any(axis=1)]

    metadata['id'] = pd.to_numeric(metadata['id'], errors ='coerce')
    metadata = metadata[metadata['id'].notna()]

    #nas = metadata.isna().sum()

    metadata['id'] = metadata['id'].astype(int)

    result = credits.dtypes
    result2 = keywords.dtypes
    result3 = metadata.dtypes

    movies = metadata.merge(credits, on='id')
    movies = movies.merge(keywords, on='id')
    movies = movies[movies['title'].notna()]

    movies = movies[movies['status']=="Released"]

    del credits
    del metadata
    del keywords

    #SELECT RELEVANT FEATURES
    movies = movies[['cast','crew','id','keywords','adult','belongs_to_collection',
                     'genres','overview','popularity','production_companies',
                     'release_date','runtime','tagline','title','vote_count','vote_average']]

    nas = movies.isna().sum()

    #DROP DUPLICATES
    movies = movies.drop_duplicates()
    movies = movies.drop_duplicates(subset='id', keep='first')

    io1 = ast.literal_eval(movies['genres'][0])
    io2 = ast.literal_eval(movies['belongs_to_collection'][0])
    io3 = ast.literal_eval(movies['keywords'][0])
    resultList = list(io2.items())

    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)
    movies['belongs_to_collection'] = movies['belongs_to_collection'].apply(convertfromdict)
    movies['production_companies'] = movies['production_companies'].apply(convert)

    ikl = movies['belongs_to_collection'][0]
    ijl = movies['production_companies'][0]
    result4 = movies.dtypes
    ikl2 = remove_space(ikl)

    movies['cast'] = movies['cast'].apply(convert)
    movies['cast'] = movies['cast'].apply(lambda x: x[0:5])

    io4 = ast.literal_eval(movies['crew'][0])
    movies['director'] = movies['crew'].apply(fetch_director)
    movies['producer'] = movies['crew'].apply(producer)
    movies['music_composer'] = movies['crew'].apply(fetch_music_composer)
    movies['screenplay'] = movies['crew'].apply(screenplay)
    movies['writer'] = movies['crew'].apply(writer)

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

    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + \
                     movies['cast'] + movies['director'] + movies['producer'] + movies['writer'] + \
                     movies['music_composer'] + movies['screenplay'] + movies['belongs_to_collection'] + \
                     movies['production_companies']

    mov_feat = movies.drop(columns=['overview','genres','keywords','cast','crew',
                                    'production_companies','belongs_to_collection',
                                    'director','producer','writer','screenplay','music_composer'])

    mov_feat['tags'] = mov_feat['tags'].apply(lambda x: " ".join(x))
    mov_feat['tags'] = mov_feat['tags'].apply(lambda x: x.lower())

    mov_feat['tags'] = mov_feat['tags'].apply(stem)

    cv = CountVectorizer(max_features=5000, stop_words='english')

    vector = cv.fit_transform(mov_feat['tags']).toarray()
    similarity = cosine_similarity(vector)

    #mov_feat[mov_feat['title'] == 'The Lego Movie'].index[0]

    # %%
    def recommend(movie):
        index = mov_feat[mov_feat['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        for i in distances[1:10]:
            print(mov_feat.iloc[i[0]].title)

    #jj = movies['id'].duplicated().sum()
    recommend('The Lion King')

    mov_feat.to_csv(dirname + 'movies_prep' + '.csv')
    l = 5

if __name__ == '__main__':
    prepn()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
