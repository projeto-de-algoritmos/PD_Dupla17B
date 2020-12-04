from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from rated_movies_scheduling import RatedMoviesScheduling
from flask import request
from flask import jsonify
import requests

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/schedule', methods=['POST'])
def schedule():

    # list of movie names
    movie_names = list(request.json['movie_names'])
    
    # list of movie starting times. Here we are also removing the seconds part, as we do not need it
    movie_start_times = [
        start_time.split(':')[:-1] for start_time in list(
            request.json['movie_start_times'])]

    # converting minutes into hours
    movie_start_times = [int(start_time[0]) +
                         float(start_time[1]) /
                         60 for start_time in movie_start_times]

    # list to be filled with all the movie's information
    movies = []

    # iterating throught received movies
    for movie, start_time in zip(movie_names, movie_start_times):
        
        # getting current movie's information from the omdbapi
        result = requests.get(
            "http://www.omdbapi.com/",
            params={
                "t": movie,
                "apikey": "4a83a64e"}).json()

        # appending movie information to array
        movies.append((
            start_time,  # start time of the movie
            start_time + float(result['Runtime'].split(' ')[0]) / 60, # end time of the movie
            float(result['imdbRating']), # movie rating, used as the weidght for scheduling
            result['Title'], # full movie name
            result['Poster'], # movie thumbnail ,
            f'https://www.imdb.com/title/{result["imdbID"]}' # link to imdb page
        ))

    # creating scheduler
    moviesScheduling = RatedMoviesScheduling(movies)

    # executing scheduling and getting the best schedule
    best_schedule = moviesScheduling.select_optimal_schedule()[1]

    return render_template(
        'scheduling_result.html',
        best_schedule=best_schedule)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
