from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask_cors import CORS
from flask_cors import cross_origin
import pandas as pd 
import datetime

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route("/")
def index():
    return "Netflix Wrapped - Server"


@cross_origin(supports_credentials=True)
@app.route("/get_data", methods=['POST'])
def get_data():
    timeFrame = request.form['timeFrame']
    userViewingHistory = request.files['file']
    userViewingHistory = pd.read_csv(userViewingHistory)
    curate = curateData(timeFrame)
    return jsonify({
        'shows': (curate['shows'].to_csv(path_or_buf=None)),
        'movies': ((curate['movies'].to_csv(path_or_buf=None))),
        'statistics': (curate['basic stats'])
    })
    
    # return jsonify({
    #     'S': curate['shows'].to_json(orient = 'records')
    # })
    # return curate['shows']


def curateData(timeFrame):
    userViewingHistory = processViewingHistory(timeFrame)[0]
    analyzedData = analyzViewingHistory(
        userViewingHistory['shows'], 
        userViewingHistory['movies']
        )
    return analyzedData


def processViewingHistory(timeFrame):
    # Date range spanning 2020
    start_date = timeFrame + "-01-01"
    end_date = timeFrame + "-12-31"
    # Netflix shows and movies dataset
    netflix_shows = pd.read_csv(r'./datasets/netflix_shows.csv') # 1969 rows
    netflix_movies = pd.read_csv(r'./datasets/netflix_movies.csv') # 4265 rows
    # User's viewing history
    df = pd.read_csv(r'NetflixViewingHistory.csv')
    # Get watch history for specified year
    dates = df[df.Date >= start_date]
    df = dates[dates.Date <= end_date]
    # Devise new column for day of week
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['day_of_week'] = df['Date'].dt.day_name() # df['day_of_week'] = df['Date'].dt.weekday
    df['month'] = df['Date'].dt.month_name() # df['day_of_week'] = df['Date'].dt.month
    # Split between TV shows and movies based on title 
    df['Shows'] = df['Title'].str.split(':',2)
    df['len'] = df['Shows'].str.len()
    shows = df[df['len'] == 3]
    movies = df[df['len'] != 3]
    # Build new columns for Shows - Title, Season, Episode
    shows = shows.join(shows['Title'].str.split(':', 2, expand=True).rename(columns={0:'title', 1:'season', 2:'episode'}))
    movies['title'] = movies['Title']
    # Add runtime for shows
    shows_rt = pd.merge(shows, netflix_shows, on='title', how='left')
    # Add runtime for movies
    movies_rt = pd.merge(movies, netflix_movies, on='title', how='left')
    return [{
        'shows': shows_rt,
        'movies': movies_rt
    }]


def analyzViewingHistory(shows, movies):
    # Total Unique Titles
    grouped_titles_movies = movies['title'].value_counts()
    grouped_titles_shows = shows['title'].value_counts()
    grouped_total = grouped_titles_movies + grouped_titles_shows 
    # Movies
    duration_movies_min = int(movies['runtimeMinutes'].sum())
    duration_movies_str = datetime.timedelta(minutes=duration_movies_min)
    # Shows 
    duration_shows_min = int(shows['runtimeMinutes'].sum())
    duration_shows_str = datetime.timedelta(minutes=duration_shows_min)
    # Total Time
    totalTime_min = duration_movies_min + duration_shows_min
    totalTime_str = datetime.timedelta(minutes=totalTime_min)
    # Day-by-Day
    per_day_shows = shows.groupby(['day_of_week'], as_index=False).sum()
    per_day_shows['runtimeMinutes_s'] = per_day_shows['runtimeMinutes']
    per_day_shows = per_day_shows[['day_of_week', 'runtimeMinutes_s']]
    per_day_movies = movies.groupby(['day_of_week'], as_index=False).sum()
    per_day_movies['runtimeMinutes_m'] = per_day_movies['runtimeMinutes']
    per_day_movies = per_day_movies[['day_of_week', 'runtimeMinutes_m']]
    per_day = pd.merge(per_day_shows, per_day_movies, on='day_of_week', how='outer').fillna(0)
    per_day['runtimeMinutes_t'] = per_day['runtimeMinutes_s'] + per_day['runtimeMinutes_m']
    days = {
        "Monday":0,
        "Tuesday":0,
        "Wednesday":0,
        "Thursday":0,
        "Friday":0,
        "Saturday":0,
        "Sunday":0,
    }
    for day in days:
        days[day] = float(per_day.loc[per_day['day_of_week']==day, 'runtimeMinutes_t'])
    return {
        "basic stats": {
            "watched_t": 60,
            "time_spent_t": str(totalTime_str),
        },
        "shows": shows,
        "movies": movies
    }


if __name__ == '__main__':
    app.run(debug=True)

























