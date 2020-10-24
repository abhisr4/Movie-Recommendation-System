from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import pandas as pd
from processing import process_movie_data, process_rating_data, recommender_system
app=Flask(__name__)
api=Api(app)
"""input=[{'title':'Breakfast Club, The', 'rating':5},
            {'title':'Toy Story', 'rating':3.5},
            {'title':'Jumanji', 'rating':2},
            {'title':"Pulp Fiction", 'rating':5},
            {'title':'Akira', 'rating':4.5}]
"""
class recommend(Resource):
    def get(self): # for get request
        return jsonify({"message":"Get request->invalid"})
    def post(self): # for post request
        inputMovies=request.get_json()
        recommendation = recommender_system(inputMovies, movies, encoded_movies, ratings)
        recommendation = recommendation.to_json(orient="records")
        return recommendation

api.add_resource(recommend,'/')
# Press the green button in the gutter to run the script.

if __name__ =="__main__":
    movies=pd.read_excel("movies.xlsx")
    ratings=pd.read_csv("ratings.csv")
    movies,encoded_movies=process_movie_data(movies)
    ratings=process_rating_data(ratings)
    app.run(debug=True)