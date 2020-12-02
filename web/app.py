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
    movie_names = list(request.json['movie_names'])
    movie_start_times = [
        start_time.split(':')[
            :-
            1] for start_time in list(
            request.json['movie_start_times'])]
    movie_start_times = [int(start_time[0]) +
                         float(start_time[1]) /
                         60 for start_time in movie_start_times]

    movies = []

    for movie, start_time in zip(movie_names, movie_start_times):
        result = requests.get(
            "http://www.omdbapi.com/",
            params={
                "t": movie,
                "apikey": "4a83a64e"}).json()
        movies.append((
            start_time,  # start time of the movie
            # end time of the movie
            start_time + float(result['Runtime'].split(' ')[0]) / 60,
            float(result['imdbRating']),
            # Rating, used as the weidght for scheduling
            result['Title'],  # full movie name
            result['Poster']
        ))

    moviesScheduling = RatedMoviesScheduling(movies)
    best_schedule = moviesScheduling.weighted_interval()[1]

    return render_template(
        'scheduling_result.html',
        best_schedule=best_schedule)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
