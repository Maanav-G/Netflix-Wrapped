from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask_cors import CORS
from flask_cors import cross_origin
import pandas as pd 
import datetime
import numpy as np
import json

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route("/")
def index():
    return "Netflix Wrapped - Server"

@cross_origin(supports_credentials=True)
@app.route("/get_data", methods=['POST'])
def get_data():
    timeFrame = request.form['timeFrame']
    userViewingHistory = pd.DataFrame(json.loads(request.form['userData']))
    # userViewingHistory = pd.read_csv(userViewingHistory)
    curate = curateData(userViewingHistory, timeFrame)    
    # return {
    #         'shows': curate['shows'].to_json(orient = 'records'),
    #         'movies': curate['movies'].to_json(orient = 'records'),
    #         'statistics': (curate['basic stats'])
    #     } 
    return jsonify(1)

def curateData(userData, timeFrame):
    userViewingHistory = processViewingHistory(userData, timeFrame)[0]
    analyzedData = analyzViewingHistory(
        userViewingHistory['shows'], 
        userViewingHistory['movies']
        )
    # return analyzedData


def processViewingHistory(userData, timeFrame):
    # Date range spanning 2020
    start_date = timeFrame + "-01-01"
    end_date = timeFrame + "-12-31"

    # User's viewing history
    df = userData
    # Get watch history for specified year
    dates = df[df.dateStr >= start_date]
    df = dates[dates.dateStr <= end_date]

    # Devise new column for day of week
    df['DateTime'] = pd.to_datetime(df['dateStr'], errors='coerce')
    df['day_of_week'] = df['DateTime'].dt.day_name() # df['day_of_week'] = df['DateTime'].dt.weekday
    df['month'] = df['DateTime'].dt.month_name() # df['day_of_week'] = df['DateTime'].dt.month

    # Split between TV shows and movies based on a lack of series
    # TODO - Find a more robust way to split dataset... 
    shows = df[df['series'].notna()]
    movies = df[df['series'].isna()]

    return [{
        'shows': shows,
        'movies': movies
    }]


def analyzViewingHistory(shows, movies):
    # Total Unique Titles
    grouped_titles_movies = movies['videoTitle'].value_counts()
    grouped_titles_shows = shows['seriesTitle'].value_counts()
    grouped_total = grouped_titles_movies + grouped_titles_shows 
    # Num Movies
    num_movies = shows['seriesTitle'].nunique()
    print("num_movies: " + num_movies)
    # Movies Duration
    duration_movies_min = int(movies['duration'].sum())
    duration_movies_str = datetime.timedelta(minutes=duration_movies_min)
    # Shows Duration
    duration_shows_min = int(shows['duration'].sum())
    duration_shows_str = datetime.timedelta(minutes=duration_shows_min)
    # Total Time
    totalTime_min = duration_movies_min + duration_shows_min
    totalTime_str = datetime.timedelta(minutes=totalTime_min)
    # Day-by-Day
    per_day_shows = shows.groupby(['day_of_week'], as_index=False).sum()
    # print("per_day_shows: " + per_day_shows)
    per_day_shows['duration_s'] = per_day_shows['duration']
    per_day_shows = per_day_shows[['day_of_week', 'duration_s']]
    per_day_movies = movies.groupby(['day_of_week'], as_index=False).sum()
    per_day_movies['duration_m'] = per_day_movies['duration']
    per_day_movies = per_day_movies[['day_of_week', 'duration_m']]
    per_day = pd.merge(per_day_shows, per_day_movies, on='day_of_week', how='outer').fillna(0)
    per_day['duration_t'] = per_day['duration_s'] + per_day['duration_m']
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
        days[day] = float(per_day.loc[per_day['day_of_week']==day, 'duration_t'])
    
    shows = shows.replace(r'^\s*$', np.nan, regex=True)
    movies = movies.replace(r'^\s*$', np.nan, regex=True)
    print(days)
    return {
        "basic stats": {
            "watched_t": 60,
            "time_spent_t": totalTime_str,
            "time_spent_m": duration_movies_str,
            "time_spent_s": duration_shows_str,
            "days": days
        },
        "shows": shows,
        "movies": movies
    }


if __name__ == '__main__':
    app.run(debug=True)

























