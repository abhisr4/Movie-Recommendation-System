import pandas as pd
from math import sqrt
def process_movie_data(movies_df):
    #movies_df=pd.read_excel("movies.xlsx")
    movies_df['year'] = movies_df.title.str.extract('(\(\d\d\d\d\))',expand=False)
    movies_df['year'] = movies_df.year.str.extract('(\d\d\d\d)',expand=False)
    movies_df['title'] = movies_df.title.str.replace('(\(\d\d\d\d\))', '')
    movies_df['title'] = movies_df['title'].apply(lambda x: x.strip())

    movies_df['genres']=movies_df.genres.str.split('|')

    movies_with_genres_df=movies_df.copy()
    for index, row in movies_df.iterrows():
        for genres in row['genres']:
            movies_with_genres_df.at[index,genres]=1
    movies_with_genres_df=movies_with_genres_df.fillna(0)

    return movies_df, movies_with_genres_df
    #return movies data without one hot encoding and with one hot encoding


def process_rating_data(ratings_df):
    #ratings_df=pd.read_csv("ratings.csv")
    #ratings_df=ratings_df.drop("timestamp",axis=1)
    return ratings_df

def recommender_system(userInput,movies_df,movies_with_genres_df,ratings_df):
    #inputMovies=pd.DataFrame(userInput)
    inputMovies=pd.json_normalize(userInput)
    inputId = movies_df[movies_df['title'].isin(inputMovies['title'].tolist())]
    inputMovies = pd.merge(inputId, inputMovies)
    inputMovies = inputMovies.drop('genres', 1).drop('year', 1)
    userMovies = movies_with_genres_df[movies_with_genres_df['movieId'].isin(inputMovies['movieId'].tolist())]
    userMovies = userMovies.reset_index(drop=True)
    userGenreTable = userMovies.drop('movieId', 1).drop('title', 1).drop('genres', 1).drop('year', 1)
    userProfile = inputMovies['rating'].transpose().dot(userGenreTable)
    genreTable = movies_with_genres_df.set_index(movies_with_genres_df['movieId'])
    genreTable = genreTable.drop('movieId', 1).drop('title', 1).drop('genres', 1).drop('year', 1)
    recommendationTable_df = ((genreTable*userProfile).sum(axis=1))/(userProfile.sum())
    recommendationTable_df = recommendationTable_df.sort_values(ascending=False)
    return movies_df.loc[movies_df['movieId'].isin(recommendationTable_df.head(5).keys())]

#debug purpose-> no issues
#t0=time.time()
#x,y=process_movie_data()
#b=process_rating_data()
"""userInput = [
            {'title':'Breakfast Club, The', 'rating':5},
            {'title':'Toy Story', 'rating':3.5},
            {'title':'Jumanji', 'rating':2},
            {'title':"Pulp Fiction", 'rating':5},
            {'title':'Akira', 'rating':4.5}
         ]"""
"""with open('data.json') as f:
    a=json.load(f)
print(recommender_system(a,x,y,b))
"""
